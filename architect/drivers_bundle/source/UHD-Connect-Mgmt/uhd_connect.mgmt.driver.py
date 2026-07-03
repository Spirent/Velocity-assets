"""
Velocity UHD Connect Management Driver.

REST wrapper around uhd_connect_rest.UHDConnectDriver with Velocity JSON shapes.
Reservation lifecycle: setup (manual RS-FEC), verifyReady (link_up poll), teardown (restore snapshot).

Author: rakesh.kumar@keysight.com
Written and debugged by rakesh.kumar@keysight.com
Co-authored-by: Cursor
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path

from uhd_connect_rest import UHDConnectDriver, unbracket_host

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
logger.addHandler(ch)

_STATE_DIR = Path(os.environ.get('UHD_CONNECT_STATE_DIR', '/tmp/velocity_uhd_connect'))


def _parse_bool(value, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')


def _parse_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def velocity_error(message: str) -> dict:
    return {'status': 'error', 'message': message}


class UHDConnectMgmtDriver:
    """Velocity-facing wrapper for UHD Connect REST operations."""

    def __init__(
        self,
        ip: str,
        username: str = 'admin',
        password: str = '',
        *,
        timeout: int = 30,
        default_port: int = 1,
        link_speed_gbps: int = 400,
        fec_mode: str = 'reed_solomon',
        verify_timeout: int = 120,
        clear_config_on_teardown: bool = False,
        reservation_id: str = '',
    ):
        self.ip = (ip or '').strip()
        self.username = username or 'admin'
        self.password = password or ''
        self.default_port = default_port
        self.link_speed_gbps = link_speed_gbps
        self.fec_mode = (fec_mode or 'reed_solomon').strip()
        self.verify_timeout = verify_timeout
        self.clear_config_on_teardown = clear_config_on_teardown
        self.reservation_id = reservation_id or ''
        self._driver = UHDConnectDriver(self.ip, timeout=timeout)

    @property
    def _state_path(self) -> Path:
        host = re.sub(r'[^a-zA-Z0-9._-]+', '_', unbracket_host(self.ip))
        suffix = self.reservation_id[:8] if self.reservation_id else 'default'
        return _STATE_DIR / f'{host}_{suffix}.json'

    def _port_status(self, link_state: str) -> str:
        return 'online' if (link_state or '').lower() == 'up' else 'offline'

    def _velocity_port_row(self, port: dict) -> dict:
        display = str(port.get('port_display') or port.get('front_panel_port') or '')
        logical = (port.get('logical_name') or '').strip()
        link = (port.get('link_state') or 'unknown').upper()
        container_parts = [f'link={link}']
        if logical:
            container_parts.append(f'name={logical}')
        if port.get('port_name'):
            container_parts.append(str(port.get('port_name')))
        row = {
            'name': display,
            'status': self._port_status(port.get('link_state', '')),
            'container': ' '.join(container_parts),
        }
        if logical:
            row['logical_name'] = logical
        return row

    def _save_checkpoint(self, config: dict | None) -> None:
        _STATE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            'reservation_id': self.reservation_id,
            'host': unbracket_host(self.ip),
            'saved_at': time.time(),
            'config': config if isinstance(config, dict) else {},
        }
        self._state_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')

    def _load_checkpoint(self) -> dict | None:
        if not self._state_path.is_file():
            return None
        try:
            data = json.loads(self._state_path.read_text(encoding='utf-8'))
            cfg = data.get('config')
            return cfg if isinstance(cfg, dict) else {}
        except Exception:
            return None

    def setup(self, args=None):
        """Apply 400G manual RS-FEC on a front-panel port (default from properties)."""
        args = args or []
        port = _parse_int(args[0], self.default_port) if args else self.default_port
        speed = _parse_int(args[1], self.link_speed_gbps) if len(args) > 1 else self.link_speed_gbps
        if len(args) > 2:
            self.reservation_id = str(args[2])

        start = time.time()
        cfg_res = self._driver.get_config()
        prior = cfg_res.data if cfg_res.success and isinstance(cfg_res.data, dict) else {}
        self._save_checkpoint(prior)

        if self.fec_mode.lower() in ('reed_solomon', 'rs', 'manual_rs'):
            apply_res = self._driver.apply_manual_rs_fec(port, speed_gbps=speed)
        else:
            return velocity_error(f'Unsupported fec_mode: {self.fec_mode}')

        if not apply_res.success:
            return velocity_error(apply_res.error or 'apply_manual_rs_fec failed')

        ready = self.verifyReady([str(port)])
        elapsed = round(time.time() - start, 1)
        return {
            'status': 'ready' if ready.get('status') == 'all_up' else 'degraded',
            'host': unbracket_host(self.ip),
            'port': port,
            'speed_gbps': speed,
            'fec_mode': self.fec_mode,
            'reservation_id': self.reservation_id,
            'setup_time_s': elapsed,
            'verifyReady': ready,
        }

    def verifyReady(self, args=None):
        """Poll metrics until the configured port reports link_up."""
        args = args or []
        port = _parse_int(args[0], self.default_port) if args else self.default_port
        deadline = time.time() + self.verify_timeout
        last_status = 'unknown'
        while time.time() < deadline:
            res = self._driver.link_status_for_port(port)
            if res.success and isinstance(res.data, dict):
                last_status = str(res.data.get('link_status') or res.data.get('link_state') or 'unknown')
                if last_status.lower() in ('link_up', 'up'):
                    return {
                        'status': 'all_up',
                        'port': port,
                        'link_status': last_status,
                        'elapsed_s': round(self.verify_timeout - (deadline - time.time()), 1),
                    }
            time.sleep(5)
        return {
            'status': 'timeout',
            'port': port,
            'link_status': last_status,
            'verify_timeout_s': self.verify_timeout,
        }

    def teardown(self, args=None):
        """Restore pre-reservation Connect config snapshot (never PUT {} unless configured)."""
        start = time.time()
        restored = False
        warnings: list[str] = []

        checkpoint = self._load_checkpoint()
        if checkpoint is not None:
            if checkpoint:
                res = self._driver.post_config(checkpoint)
            else:
                res = self._driver.put_config({})
            if res.success:
                restored = True
            else:
                warnings.append(res.error or 'config restore failed')
        elif self.clear_config_on_teardown:
            res = self._driver.put_config({})
            if res.success:
                restored = True
            else:
                warnings.append(res.error or 'clear config failed')
        else:
            warnings.append('no checkpoint found; left active config unchanged')

        if self._state_path.is_file():
            try:
                self._state_path.unlink()
            except OSError:
                pass

        return {
            'status': 'released' if not warnings else 'released_with_warnings',
            'host': unbracket_host(self.ip),
            'restored': restored,
            'teardown_time_s': round(time.time() - start, 1),
            'warnings': warnings,
        }

    def getVlans(self, args=None):
        """L2 interface stub — UHD Connect has no VLAN API."""
        return {'vlans': []}

    def applyLayer1Profile(self, args=None):
        """Custom procedure: applyLayer1Profile <port> [speedGbps]."""
        args = args or []
        if not args:
            return velocity_error('applyLayer1Profile requires port')
        port = _parse_int(args[0], self.default_port)
        speed = _parse_int(args[1], self.link_speed_gbps) if len(args) > 1 else self.link_speed_gbps
        res = self._driver.apply_manual_rs_fec(port, speed_gbps=speed)
        if not res.success:
            return velocity_error(res.error or 'applyLayer1Profile failed')
        return {'status': 'ok', 'port': port, 'speed_gbps': speed, 'fec_mode': 'reed_solomon'}

    def setConfig(self, args=None):
        """CONFIGURABLE interface — apply manual RS-FEC (delegates to setup).

        Velocity passes -fileSize/-url for the config asset; the JSON profile is a
        marker only. L1 values come from inventory driver properties.
        """
        return self.setup()

    def getConfig(self, args=None):
        res = self._driver.get_config()
        if not res.success:
            return velocity_error(res.error or 'getConfig failed')
        return {'status': 'ok', 'config': res.data if isinstance(res.data, dict) else {}}

    def getProperties(self, args=None):
        args = args or []
        include_ports = False
        if args:
            if args[0] in ('true', '-includePorts'):
                include_ports = True
            elif len(args) >= 2 and args[0] == '-includePorts' and args[1].lower() == 'true':
                include_ports = True

        props = {
            'Hostname': unbracket_host(self.ip),
            'Make': 'Keysight',
            'Model': 'UHD Connect',
            'SerialNumber': '',
            'ManagementIPv4': unbracket_host(self.ip),
            'Platform': 'KCOS',
        }

        config_res = self._driver.get_config()
        if config_res.success and isinstance(config_res.data, dict):
            fp = config_res.data.get('front_panel_ports') or []
            conns = config_res.data.get('connections') or []
            props['ConfiguredFrontPanelPorts'] = str(len(fp))
            props['ConfiguredConnections'] = str(len(conns))

        result = {'properties': props}
        if include_ports:
            ports_result = self.getPorts()
            if 'ports' in ports_result:
                result['ports'] = ports_result['ports']
            elif ports_result.get('status') == 'error':
                result['ports_error'] = ports_result.get('message', '')
        return result

    def getPorts(self, args=None):
        ports_res = self._driver.get_ports()
        if not ports_res.success:
            return {'status': 'error', 'message': ports_res.error or 'Failed to fetch ports'}
        port_list = [self._velocity_port_row(p) for p in (ports_res.data or [])]
        return {'ports': port_list}

    def getLldpNeighbors(self, args=None):
        return {'neighbors': []}

    def getHealth(self, args=None):
        hres = self._driver.get_health()
        if not hres.success:
            return {'status': 'error', 'message': hres.error or 'get_health failed'}
        return {'status': 'ok', 'health': hres.data or {}}

    def getMetrics(self, args=None):
        res = self._driver.query_metrics()
        if not res.success:
            return {'status': 'error', 'message': res.error or 'metrics query failed'}
        return {'status': 'ok', 'metrics': res.data or {}}

    def getSensors(self, args=None):
        return {'status': 'ok', 'sensors': []}

    def getCards(self, args=None):
        return {'status': 'ok', 'cards': [{'card_number': 1, 'type': 'UHD Connect', 'port_count': 32}]}

    def healthcheck(self, args=None):
        health = {'status': 'ok'}
        issues: list[str] = []

        ports_res = self._driver.get_ports()
        if not ports_res.success:
            return {'status': 'error', 'message': ports_res.error or 'metrics query failed'}
        ports = ports_res.data if isinstance(ports_res.data, list) else []
        summary = self._driver.summarize_port_health(ports)
        health['ports'] = summary
        if summary.get('ports_down', 0) > summary.get('ports_up', 0):
            issues.append('majority_ports_down')
        if summary.get('total_ports', 0) == 0:
            issues.append('no_ports_reported')

        hres = self._driver.get_health()
        if hres.success and isinstance(hres.data, dict):
            health['chassis'] = hres.data

        if issues:
            health['status'] = 'degraded'
            health['issues'] = issues
        return health

    def linkCheck(self, args=None):
        port_name = (args or [''])[0] if args else ''
        res = self._driver.link_check(port_name)
        if not res.success:
            return {'status': 'error', 'message': res.error or 'linkCheck failed'}
        links = (res.data or {}).get('links') or []
        down = [r for r in links if not r.get('link_up')]
        status = 'ok' if not down else 'degraded'
        return {'status': status, 'links': links, 'ports_down': len(down), 'ports_checked': len(links)}

    def takeOwnership(self, args=None):
        return {
            'status': 'ok',
            'message': 'UHD Connect has no port ownership API; operation is a no-op',
            'port': (args or [''])[0] if args else '',
        }

    def releaseOwnership(self, args=None):
        return {
            'status': 'ok',
            'message': 'UHD Connect has no port ownership API; operation is a no-op',
            'port': (args or [''])[0] if args else '',
        }

    def runCommand(self, args=None):
        return {
            'output': '',
            'error': 'runCommand not supported for UHD Connect (REST-only driver)',
        }

    def probe(self, args=None):
        return {'status': self._driver.probe()}


DISPATCH = {
    'getProperties': 'getProperties',
    'getPorts': 'getPorts',
    'getVlans': 'getVlans',
    'getLldpNeighbors': 'getLldpNeighbors',
    'getHealth': 'getHealth',
    'getMetrics': 'getMetrics',
    'getSensors': 'getSensors',
    'getCards': 'getCards',
    'healthcheck': 'healthcheck',
    'linkCheck': 'linkCheck',
    'takeOwnership': 'takeOwnership',
    'releaseOwnership': 'releaseOwnership',
    'runCommand': 'runCommand',
    'probe': 'probe',
    'setup': 'setup',
    'teardown': 'teardown',
    'verifyReady': 'verifyReady',
    'setConfig': 'setConfig',
    'getConfig': 'getConfig',
    'applyLayer1Profile': 'applyLayer1Profile',
}


def _env_properties() -> dict:
    props = {}
    for key, val in os.environ.items():
        if key.startswith('VELOCITY_PARAM_property_'):
            props[key.replace('VELOCITY_PARAM_property_', '', 1)] = val
    if 'VELOCITY_PARAM_RESERVATION_ID' in os.environ:
        props['reservation_id'] = os.environ['VELOCITY_PARAM_RESERVATION_ID']
    return props


def _build_driver() -> UHDConnectMgmtDriver:
    props = _env_properties()
    return UHDConnectMgmtDriver(
        props.get('ipAddress', props.get('Hostname', '')),
        props.get('username', 'admin'),
        props.get('password', ''),
        timeout=_parse_int(props.get('timeout'), 30),
        default_port=_parse_int(props.get('defaultPort'), 1),
        link_speed_gbps=_parse_int(props.get('linkSpeedGbps'), 400),
        fec_mode=str(props.get('fecMode') or 'reed_solomon'),
        verify_timeout=_parse_int(props.get('verifyTimeout'), 120),
        clear_config_on_teardown=_parse_bool(props.get('clearConfigOnTeardown'), False),
        reservation_id=str(props.get('reservation_id') or ''),
    )


def _run_velocity_dispatch():
    driver = _build_driver()

    for call_number in range(int(os.environ['VELOCITY_PARAM_call_count'])):
        env_var = os.environ['VELOCITY_PARAM_call_' + str(call_number)]
        parts = env_var.split()
        call_name = parts[0] if parts else ''
        call_args = parts[1:] if len(parts) > 1 else []

        method_name = DISPATCH.get(call_name)
        if method_name is None:
            ret_val = velocity_error(f'Unknown command: {call_name}')
        else:
            handler = getattr(driver, method_name)
            ret_val = handler(call_args) if call_args else handler()

        print(json.dumps(ret_val))


if 'VELOCITY_PARAM_call_count' in os.environ:
    _run_velocity_dispatch()
