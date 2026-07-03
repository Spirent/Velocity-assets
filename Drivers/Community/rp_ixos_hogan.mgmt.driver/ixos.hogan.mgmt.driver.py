"""
Velocity AresONE / IxOS Hogan Management Driver.

REST + SSH wrapper around ixos_rest.IxOSDriver with Velocity JSON return shapes.

Author: rakesh.kumar@keysight.com
Written and debugged by rakesh.kumar@keysight.com
Co-authored-by: Cursor
"""
from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

from ixos_rest import IxOSDriver

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
# Do not attach StreamHandler — stdout must be JSON-only for Velocity agent dispatch.


def _parse_bool(value, default=True) -> bool:
    if value is None or value == '':
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')


def _rest_disabled_error(operation: str) -> dict:
    return {
        'status': 'error',
        'message': f'REST disabled; operation requires REST: {operation}',
    }


class IxOSHoganDriver:
    """Velocity-facing wrapper for IxOS REST + SSH operations."""

    def __init__(
        self,
        ip: str,
        username: str = 'admin',
        password: str = '',
        *,
        api_username: str = '',
        api_password: str = '',
        chassis_type: str = '',
        use_rest_api: bool = True,
        hostname: str = '',
    ):
        self.ip = (ip or '').strip()
        self.username = username or 'admin'
        self.password = password or ''
        self.use_rest_api = use_rest_api
        rest_user = (api_username or '').strip() or self.username
        rest_pass = (api_password or '').strip() or self.password
        self._driver = IxOSDriver(
            self.ip,
            rest_user,
            rest_pass,
            hostname=hostname,
            chassis_type=chassis_type,
        )

    def _port_status(self, link_state: str) -> str:
        return 'online' if (link_state or '').lower() == 'up' else 'offline'

    @staticmethod
    def _port_field_str(value: Any, default: str = '') -> str:
        if value is None:
            return default
        return str(value).strip() or default

    def _velocity_port_row(self, port: dict, display_name: str | None = None) -> dict:
        name = display_name or port.get('port_display') or str(port.get('port_number', ''))
        speed = self._port_field_str(port.get('speed') or port.get('type'), 'Unknown')
        owner = self._port_field_str(port.get('owner'), 'Free') or 'Free'
        rg = port.get('resource_group_number')
        rg_label = f' RG{rg}' if rg is not None else ''
        mgmt = self._port_field_str(port.get('management_ip'))
        mgmt_suffix = f' pcpu={mgmt}' if mgmt else ''
        container = f'{speed}{rg_label} owner={owner}{mgmt_suffix}'.strip()
        row = {
            'name': name,
            'status': self._port_status(port.get('link_state', '')),
            'container': container,
        }
        if port.get('management_ip_inferred'):
            row['management_ip_inferred'] = True
        if mgmt:
            row['management_ip'] = mgmt
        if owner and owner != 'Free':
            row['owner'] = owner
        return row

    def _resolve_port_id(self, port_name: str) -> tuple[int | None, str]:
        """Resolve display name (e.g. 1.1) to REST port id."""
        target = (port_name or '').strip()
        if not target:
            return None, ''

        if self.use_rest_api:
            ports_res = self._driver.get_ports()
            if ports_res.success and isinstance(ports_res.data, list):
                topo_map = self._build_display_map(ports_res.data)
                for p in ports_res.data:
                    cn = p.get('card_number', 0)
                    pn = p.get('port_number', 0)
                    display = topo_map.get((cn, pn)) or p.get('port_display') or f'{cn}.{pn}'
                    if display == target or str(p.get('port_number')) == target:
                        return int(p.get('id', 0) or 0), display

        topo_res = self._driver.get_topology_ssh()
        if topo_res.success and isinstance(topo_res.data, dict):
            for card_info in (topo_res.data.get('cards') or {}).values():
                for rg in card_info.get('resource_groups') or []:
                    for p in rg.get('ports') or []:
                        if p.get('display') == target:
                            return None, target

        return None, target

    def _build_display_map(self, rest_ports: list) -> dict:
        mapping = {}
        for p in rest_ports:
            cn = p.get('card_number', 0)
            pn = p.get('port_number', 0)
            if p.get('port_display'):
                mapping[(cn, pn)] = p.get('port_display')
        if mapping:
            return mapping
        topo_res = self._driver.get_topology_ssh()
        if topo_res.success and isinstance(topo_res.data, dict):
            return self._driver.correlate_ports(topo_res.data, rest_ports)
        for p in rest_ports:
            cn = p.get('card_number', 0)
            pn = p.get('port_number', 0)
            mapping[(cn, pn)] = p.get('port_display') or f'{cn}.{pn}'
        return mapping

    def _ports_from_rest(self) -> dict:
        ports_res = self._driver.get_ports()
        if not ports_res.success:
            return {'status': 'error', 'message': ports_res.error or 'Failed to fetch ports'}
        rest_ports = ports_res.data if isinstance(ports_res.data, list) else []
        display_map = self._build_display_map(rest_ports)
        port_list = []
        for p in rest_ports:
            cn = p.get('card_number', 0)
            pn = p.get('port_number', 0)
            display = display_map.get((cn, pn)) or p.get('port_display') or f'{cn}.{pn}'
            port_list.append(self._velocity_port_row(p, display))
        return {'ports': port_list}

    def _ports_from_ssh(self) -> dict:
        topo_res = self._driver.get_topology_ssh()
        if not topo_res.success:
            return {'status': 'error', 'message': topo_res.error or 'SSH topology failed'}
        port_list = []
        for card_info in (topo_res.data.get('cards') or {}).values():
            for rg in card_info.get('resource_groups') or []:
                mode = (rg.get('mode') or '').strip()
                for p in rg.get('ports') or []:
                    link = (p.get('link') or '').lower()
                    status = 'online' if link == 'up' else 'offline'
                    container = (p.get('type') or mode or 'Unknown').strip() or 'Unknown'
                    port_list.append({
                        'name': p.get('display', ''),
                        'status': status,
                        'container': container,
                    })
        return {'ports': port_list}

    def _properties_from_rest(self) -> dict:
        info_res = self._driver.get_chassis_info()
        if not info_res.success:
            return {}
        info = info_res.data if isinstance(info_res.data, dict) else {}
        model = (info.get('chassis_type') or '').replace('_', ' ').strip()
        return {
            'Hostname': unbracket_host(self.ip) if hasattr(self, 'ip') else self.ip,
            'Make': 'Ixia',
            'Model': model,
            'SerialNumber': info.get('serial_number', ''),
            'IxOSVersion': info.get('ixos_version', ''),
            'ChassisStatus': info.get('state', ''),
            'ManagementIPv4': unbracket_host(info.get('management_ip', self.ip)),
        }

    def _properties_from_ssh(self) -> dict:
        props = {
            'Hostname': self.ip,
            'Make': 'Ixia',
            'Model': '',
            'SerialNumber': '',
            'IxOSVersion': '',
            'ChassisStatus': '',
            'ManagementIPv4': self.ip,
        }
        welcome = self._driver._ssh_run('show welcome-screen', timeout=15)
        for line in (welcome or '').splitlines():
            m = re.match(r'\|\s*(.+?)\s*:\s*(.+?)\s*\|', line)
            if not m:
                continue
            key = m.group(1).strip().lower()
            val = m.group(2).strip()
            if 'management ipv4' in key:
                props['ManagementIPv4'] = val
            elif 'active ixos version' in key:
                props['IxOSVersion'] = val
            elif 'chassis status' in key:
                props['ChassisStatus'] = val

        topo_res = self._driver.get_topology_ssh()
        if topo_res.success and isinstance(topo_res.data, dict):
            cards = topo_res.data.get('cards') or {}
            if cards:
                first = next(iter(cards.values()))
                props['SerialNumber'] = first.get('serial', '')
        raw_topo = self._driver._ssh_run('show topology', timeout=12)
        for line in (raw_topo or '').splitlines():
            m = re.match(r'^(.+?)\s+\(ChassisSN\s+(\S+)\)', line.strip())
            if m:
                props['Model'] = m.group(1).strip()
                if not props['SerialNumber']:
                    props['SerialNumber'] = m.group(2).strip()
                break
        return props

    def getProperties(self, args=None):
        args = args or []
        include_ports = False
        if args:
            if args[0] in ('true', '-includePorts'):
                include_ports = True
            elif len(args) >= 2 and args[0] == '-includePorts' and args[1].lower() == 'true':
                include_ports = True

        if self.use_rest_api:
            props = self._properties_from_rest()
            if not props and self._driver.probe() == 'auth_failed':
                return {'status': 'error', 'message': 'Authentication failed'}
        else:
            props = self._properties_from_ssh()

        result = {'properties': props}
        if include_ports:
            ports_result = self.getPorts()
            if 'ports' in ports_result:
                result['ports'] = ports_result['ports']
            elif ports_result.get('status') == 'error':
                result['ports_error'] = ports_result.get('message', '')
        if props:
            result['status'] = 'ok'
        return result

    def _ssh_topology_ok(self) -> bool:
        topo_res = self._driver.get_topology_ssh()
        return bool(topo_res.success and topo_res.data)

    def getPorts(self, args=None):
        if self.use_rest_api:
            result = self._ports_from_rest()
            if result.get('status') != 'error':
                return result
            ssh_result = self._ports_from_ssh()
            if ssh_result.get('status') == 'ok':
                return ssh_result
            return result
        return self._ports_from_ssh()

    def getLldpNeighbors(self, args=None):
        lldp_res = self._driver.get_lldp_ssh()
        peers = []
        if lldp_res.success and isinstance(lldp_res.data, list) and lldp_res.data:
            peers = lldp_res.data
        elif self.use_rest_api:
            rest_res = self._driver.get_lldp_peers()
            if rest_res.success and isinstance(rest_res.data, list):
                peers = rest_res.data

        neighbors = []
        for p in peers:
            if not isinstance(p, dict):
                continue
            neighbors.append({
                'local_port': p.get('local_port', ''),
                'remote_host': p.get('remote_device', '') or p.get('mgmt_ip', ''),
                'remote_port': p.get('remote_port', ''),
            })
        return {'neighbors': neighbors}

    def getHealth(self, args=None):
        if not self.use_rest_api:
            return _rest_disabled_error('getHealth')
        hres = self._driver.get_health()
        data = hres.data if hres.success and isinstance(hres.data, dict) else {}
        return {'status': 'ok', 'health': data}

    def getSensors(self, args=None):
        if not self.use_rest_api:
            return _rest_disabled_error('getSensors')
        sres = self._driver.get_sensors()
        return {'status': 'ok', 'sensors': sres.data if sres.success else []}

    def getCards(self, args=None):
        if not self.use_rest_api:
            return _rest_disabled_error('getCards')
        cres = self._driver.get_cards()
        if not cres.success:
            return {'status': 'error', 'message': cres.error or 'get_cards failed'}
        return {'status': 'ok', 'cards': cres.data or []}

    def _link_check_from_ssh(self, target: str) -> dict:
        ports_result = self._ports_from_ssh()
        if ports_result.get('status') == 'error':
            return ports_result
        links = []
        for row in ports_result.get('ports') or []:
            name = row.get('name', '')
            if target and name != target:
                continue
            up = (row.get('status') or '').lower() in ('online', 'up')
            links.append({
                'port': name,
                'link_state': 'up' if up else 'down',
                'link_up': up,
                'status': 'online' if up else 'offline',
            })
        down = [r for r in links if not r.get('link_up')]
        return {
            'status': 'ok' if not down else 'degraded',
            'links': links,
            'ports_down': len(down),
            'ports_checked': len(links),
        }

    def linkCheck(self, args=None):
        """Return per-port link status for Velocity inventory polling."""
        port_name = (args or [''])[0] if args else ''
        target = (port_name or '').strip()
        if self.use_rest_api:
            ports_res = self._driver.get_ports()
            if not ports_res.success:
                ssh_result = self._link_check_from_ssh(target)
                if ssh_result.get('status') != 'error':
                    return ssh_result
                return {'status': 'error', 'message': ports_res.error or 'linkCheck failed'}
            rest_ports = ports_res.data if isinstance(ports_res.data, list) else []
            display_map = self._build_display_map(rest_ports)
            links = []
            for p in rest_ports:
                cn = p.get('card_number', 0)
                pn = p.get('port_number', 0)
                display = display_map.get((cn, pn)) or p.get('port_display') or f'{cn}.{pn}'
                if target and display != target and str(pn) != target:
                    continue
                link = (p.get('link_state') or 'unknown').lower()
                is_up = link == 'up'
                links.append({
                    'port': display,
                    'link_state': link,
                    'link_up': is_up,
                    'status': 'online' if is_up else 'offline',
                })
            down = [r for r in links if not r.get('link_up')]
            return {
                'status': 'ok' if not down else 'degraded',
                'links': links,
                'ports_down': len(down),
                'ports_checked': len(links),
            }
        return self._link_check_from_ssh(target)

    def healthcheck(self, args=None):
        """Reservation health: chassis REST health + port link summary."""
        health = {'status': 'ok'}
        issues: list[str] = []
        if self.use_rest_api:
            hres = self._driver.get_health()
            if hres.success and isinstance(hres.data, dict):
                health['chassis'] = hres.data
                cpu = float(hres.data.get('cpu_utilization') or 0)
                if cpu > 90:
                    issues.append(f'high_cpu={cpu}%')
            ports_res = self._driver.get_ports()
            if ports_res.success and isinstance(ports_res.data, list):
                summary = self._driver.summarize_port_health(ports_res.data)
                health['ports'] = summary
                if summary.get('ports_down', 0) > summary.get('ports_up', 0):
                    issues.append('majority_ports_down')
        else:
            ports_result = self._ports_from_ssh()
            plist = ports_result.get('ports') or []
            down = [p for p in plist if (p.get('status') or '').lower() not in ('online', 'up')]
            health['ports'] = {'total_ports': len(plist), 'ports_down': len(down)}
            if len(down) > len(plist) // 2:
                issues.append('majority_ports_down')

        if issues:
            health['status'] = 'degraded'
            health['issues'] = issues
        return health

    def takeOwnership(self, args=None):
        if not self.use_rest_api:
            return _rest_disabled_error('takeOwnership')
        port_name = (args or [''])[0]
        port_id, display = self._resolve_port_id(port_name)
        if not port_id:
            return {'status': 'error', 'message': f'Port not found: {port_name}'}
        result = self._driver.take_ownership(port_id)
        if result.success:
            return {'status': 'ok', 'port': display or port_name}
        return {'status': 'error', 'message': result.error or 'takeOwnership failed'}

    def releaseOwnership(self, args=None):
        if not self.use_rest_api:
            return _rest_disabled_error('releaseOwnership')
        port_name = (args or [''])[0]
        port_id, display = self._resolve_port_id(port_name)
        if not port_id:
            return {'status': 'error', 'message': f'Port not found: {port_name}'}
        result = self._driver.release_ownership(port_id)
        if result.success:
            return {'status': 'ok', 'port': display or port_name}
        return {'status': 'error', 'message': result.error or 'releaseOwnership failed'}

    def rebootPort(self, args=None):
        if not self.use_rest_api:
            return _rest_disabled_error('rebootPort')
        port_name = (args or [''])[0]
        port_id, display = self._resolve_port_id(port_name)
        if not port_id:
            return {'status': 'error', 'message': f'Port not found: {port_name}'}
        result = self._driver.reboot_port(port_id)
        if result.success:
            return {'status': 'ok', 'port': display or port_name}
        return {'status': 'error', 'message': result.error or 'rebootPort failed'}

    def runCommand(self, args=None):
        if not args:
            return {'output': '', 'error': 'No command specified'}
        command = ' '.join(args)
        output = self._driver._ssh_run(command, timeout=30)
        if not output and self._driver._last_ssh_error:
            return {'output': '', 'error': self._driver._last_ssh_error}
        lines = output.splitlines()
        if len(lines) > 2:
            lines = lines[1:-1]
            output = '\n'.join(lines)
        return {'output': output}

    def probe(self, args=None):
        if self.use_rest_api:
            status = self._driver.probe()
            if status == 'ok':
                return {'status': status}
            if self._ssh_topology_ok():
                return {'status': 'ok'}
            return {'status': status}
        try:
            out = self._driver._ssh_run('show version', timeout=10)
            if out:
                return {'status': 'ok'}
            if self._driver._last_ssh_error:
                return {'status': 'auth_failed'}
            return {'status': 'unreachable'}
        except Exception:
            return {'status': 'unreachable'}

    def setup(self, args=None):
        """Optional reservation setup — takeOwnership on listed ports (comma-separated)."""
        import time
        args = args or []
        port_arg = args[0] if args else os.environ.get('VELOCITY_PARAM_property_defaultPorts', '')
        ports = [p.strip() for p in str(port_arg).split(',') if p.strip()]
        taken = []
        warnings = []
        for port in ports:
            res = self.takeOwnership([port])
            if res.get('status') == 'ok':
                taken.append(port)
            else:
                warnings.append(f"{port}: {res.get('message', res.get('status'))}")
        ready = self.verifyReady(ports or None)
        return {
            'status': 'ready' if ready.get('status') == 'all_up' else 'degraded',
            'ports_owned': taken,
            'warnings': warnings,
            'verifyReady': ready,
        }

    def verifyReady(self, args=None):
        """Poll linkCheck until ports are up or timeout."""
        import time
        targets: list[str] = []
        if args:
            if isinstance(args, list) and len(args) == 1 and ',' in str(args[0]):
                targets = [p.strip() for p in str(args[0]).split(',') if p.strip()]
            elif isinstance(args, list):
                targets = [str(a) for a in args if str(a).strip()]
        timeout_s = int(os.environ.get('VELOCITY_PARAM_property_verifyTimeout', '120') or 120)
        deadline = time.time() + timeout_s
        last = {}
        while time.time() < deadline:
            if targets:
                down = []
                for port in targets:
                    last = self.linkCheck([port])
                    links = last.get('links') or []
                    if any(not l.get('link_up') for l in links):
                        down.append(port)
                if not down:
                    return {'status': 'all_up', 'ports': targets, 'elapsed_s': round(timeout_s - (deadline - time.time()), 1)}
            else:
                last = self.linkCheck([])
                if last.get('status') == 'ok' and (last.get('ports_down') or 0) == 0:
                    return {
                        'status': 'all_up',
                        'ports_checked': last.get('ports_checked', 0),
                        'elapsed_s': round(timeout_s - (deadline - time.time()), 1),
                    }
            time.sleep(5)
        return {
            'status': 'timeout',
            'verify_timeout_s': timeout_s,
            'last_link_check': last,
        }

    def teardown(self, args=None):
        """Release ownership taken during setup."""
        args = args or []
        port_arg = args[0] if args else os.environ.get('VELOCITY_PARAM_property_defaultPorts', '')
        ports = [p.strip() for p in str(port_arg).split(',') if p.strip()]
        released = []
        warnings = []
        for port in ports:
            res = self.releaseOwnership([port])
            if res.get('status') == 'ok':
                released.append(port)
            else:
                warnings.append(f"{port}: {res.get('message', res.get('status'))}")
        return {
            'status': 'released' if not warnings else 'released_with_warnings',
            'ports_released': released,
            'warnings': warnings,
        }

    def setConfig(self, args=None):
        """Management/Configurable marker — optional ownership + link verify."""
        return self.setup(args)

    def getConfig(self, args=None):
        props = self.getProperties()
        return {'status': 'ok', 'properties': props.get('properties') or {}}


def unbracket_host(host: str) -> str:
    raw = (host or '').strip()
    if raw.startswith('[') and raw.endswith(']'):
        return raw[1:-1]
    return raw


DISPATCH = {
    'getProperties': 'getProperties',
    'getPorts': 'getPorts',
    'getLldpNeighbors': 'getLldpNeighbors',
    'getHealth': 'getHealth',
    'getSensors': 'getSensors',
    'getCards': 'getCards',
    'healthcheck': 'healthcheck',
    'linkCheck': 'linkCheck',
    'takeOwnership': 'takeOwnership',
    'releaseOwnership': 'releaseOwnership',
    'rebootPort': 'rebootPort',
    'runCommand': 'runCommand',
    'probe': 'probe',
    'setup': 'setup',
    'verifyReady': 'verifyReady',
    'teardown': 'teardown',
    'setConfig': 'setConfig',
    'getConfig': 'getConfig',
}


def _run_velocity_dispatch():
    ssh_server = os.environ['VELOCITY_PARAM_property_ipAddress']
    ssh_username = os.environ.get('VELOCITY_PARAM_property_username', 'admin')
    ssh_password = os.environ.get('VELOCITY_PARAM_property_password', '')
    chassis_type = os.environ.get('VELOCITY_PARAM_property_chassisType', '') or 'aresone'
    api_username = os.environ.get('VELOCITY_PARAM_property_apiUsername', '')
    api_password = os.environ.get('VELOCITY_PARAM_property_apiPassword', '')
    use_rest_api = os.environ.get('VELOCITY_PARAM_property_useRestApi', 'true')

    driver = IxOSHoganDriver(
        ssh_server,
        ssh_username,
        ssh_password,
        api_username=api_username,
        api_password=api_password,
        chassis_type=chassis_type,
        use_rest_api=_parse_bool(use_rest_api, default=True),
    )

    for call_number in range(int(os.environ['VELOCITY_PARAM_call_count'])):
        env_var = os.environ['VELOCITY_PARAM_call_' + str(call_number)]
        parts = env_var.split()
        call_name = parts[0] if parts else ''
        call_args = parts[1:] if len(parts) > 1 else []

        method_name = DISPATCH.get(call_name)
        if method_name is None:
            ret_val = {'status': 'error', 'message': f'Unknown command: {call_name}'}
        else:
            handler = getattr(driver, method_name)
            ret_val = handler(call_args) if call_args else handler()

        print(json.dumps(ret_val))


if 'VELOCITY_PARAM_call_count' in os.environ:
    _run_velocity_dispatch()
