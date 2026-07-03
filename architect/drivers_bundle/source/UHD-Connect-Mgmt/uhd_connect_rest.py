"""
UHD Connect REST driver (Keysight UHD Connect on KCOS).

Official docs (on each appliance):
  UI guide     : https://{ip}/
  Connect API  : https://{ip}/uhd_connect/redoc.html  -> /uhd_connect/openapi.json
  Samples      : https://{ip}/samples.tar.gz
  Ixia-C (BGP) : https://{ip}/ixiac/redoc.html        -> /ixiac/openapi.json

REST base path: https://{ip}/connect/api/v1  (see OpenAPI servers.basePath)

Published OpenAPI paths:
  GET/PUT /config

Runtime endpoints (Getting Started + samples; not all listed in OpenAPI):
  POST /metrics/operations/query  -> port_metrics.metrics[].metrics.link_status
  POST /metrics/operations/clear
  POST /control/operations/switchover  -> {"enable": true|false}

Ixia-C API (root /, separate from connect) is used for internal BGP services
when running the with_bgp sample — see /ixiac/redoc.html.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)

_CONNECT_BASE = '/connect/api/v1'
_OPENAPI_CONNECT = '/uhd_connect/openapi.json'
_OPENAPI_IXIAC = '/ixiac/openapi.json'
_session_pool: dict[str, requests.Session] = {}


def bracket_host(host: str) -> str:
    raw = (host or '').strip()
    if not raw:
        return ''
    if raw.startswith('['):
        return raw
    return raw


def unbracket_host(host: str) -> str:
    raw = (host or '').strip()
    if raw.startswith('[') and raw.endswith(']'):
        return raw[1:-1]
    return raw


@dataclass
class DriverResult:
    success: bool = False
    data: Any = None
    error: str = ''


def _get_session(ip: str) -> requests.Session:
    key = bracket_host(ip)
    if key not in _session_pool:
        s = requests.Session()
        s.verify = False
        _session_pool[key] = s
    return _session_pool[key]


class UHDConnectDriver:
    """REST client for UHD Connect appliances."""

    def __init__(self, ip: str, *, timeout: int = 30):
        self.ip = bracket_host((ip or '').strip())
        self.timeout = timeout

    @property
    def _base(self) -> str:
        return f'https://{self.ip}{_CONNECT_BASE}'

    def _get(self, path: str) -> DriverResult:
        session = _get_session(self.ip)
        url = path if path.startswith('http') else self._base + path
        try:
            resp = session.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                try:
                    return DriverResult(success=True, data=resp.json())
                except Exception:
                    return DriverResult(success=True, data=resp.text)
            return DriverResult(error=f'HTTP {resp.status_code}')
        except Exception as exc:
            return DriverResult(error=str(exc))

    def _post(self, path: str, payload: Any = None) -> DriverResult:
        session = _get_session(self.ip)
        url = path if path.startswith('http') else self._base + path
        try:
            resp = session.post(
                url,
                json=payload if payload is not None else {},
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                timeout=self.timeout,
            )
            if resp.status_code in (200, 201, 202, 204):
                if not resp.text.strip():
                    return DriverResult(success=True, data={})
                try:
                    return DriverResult(success=True, data=resp.json())
                except Exception:
                    return DriverResult(success=True, data=resp.text)
            return DriverResult(error=f'HTTP {resp.status_code}: {resp.text[:200]}')
        except Exception as exc:
            return DriverResult(error=str(exc))

    def probe(self) -> str:
        res = self.query_metrics()
        if res.success:
            return 'ok'
        err = (res.error or '').lower()
        if 'timeout' in err or 'refused' in err or 'unreachable' in err:
            return 'unreachable'
        return 'error'

    def get_config(self) -> DriverResult:
        return self._get('/config')

    def put_config(self, config: dict) -> DriverResult:
        session = _get_session(self.ip)
        url = f'{self._base}/config'
        try:
            resp = session.put(
                url,
                json=config,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                timeout=self.timeout,
            )
            if resp.status_code in (200, 204):
                return DriverResult(success=True, data=config)
            return DriverResult(error=f'HTTP {resp.status_code}: {resp.text[:200]}')
        except Exception as exc:
            return DriverResult(error=str(exc))

    def post_config(self, config: dict) -> DriverResult:
        session = _get_session(self.ip)
        url = f'{self._base}/config'
        try:
            resp = session.post(
                url,
                json=config,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                timeout=self.timeout,
            )
            if resp.status_code in (200, 201, 202, 204):
                if not resp.text.strip():
                    return DriverResult(success=True, data=config)
                try:
                    return DriverResult(success=True, data=resp.json())
                except Exception:
                    return DriverResult(success=True, data=config)
            return DriverResult(error=f'HTTP {resp.status_code}: {resp.text[:200]}')
        except Exception as exc:
            return DriverResult(error=str(exc))

    @staticmethod
    def build_manual_rs_profile(
        *,
        port: int,
        speed_gbps: int = 400,
        profile_name: str = 'manual_rs',
        logical_name: str | None = None,
    ) -> dict:
        speed_token = {
            100: 'speed_100_gbps',
            200: 'speed_200_gbps',
            400: 'speed_400_gbps',
        }.get(speed_gbps, f'speed_{speed_gbps}_gbps')
        return {
            'profiles': {
                'layer_1_profiles': [{
                    'name': profile_name,
                    'link_speed': speed_token,
                    'choice': 'manual',
                    'manual': {'fec_mode': 'reed_solomon'},
                }],
            },
            'front_panel_ports': [{
                'name': logical_name or f'fp{port}',
                'choice': 'front_panel_port',
                'front_panel_port': {
                    'front_panel_port': port,
                    'layer_1_profile_name': profile_name,
                },
            }],
        }

    def apply_manual_rs_fec(
        self,
        port: int,
        *,
        speed_gbps: int = 400,
        profile_name: str = 'manual_rs',
        logical_name: str | None = None,
    ) -> DriverResult:
        cfg = self.build_manual_rs_profile(
            port=port,
            speed_gbps=speed_gbps,
            profile_name=profile_name,
            logical_name=logical_name,
        )
        return self.post_config(cfg)

    def link_status_for_port(self, port: int) -> DriverResult:
        res = self.query_metrics({'ports': [port]})
        if not res.success:
            return res
        data = res.data if isinstance(res.data, dict) else {}
        for row in (data.get('port_metrics') or {}).get('metrics') or []:
            if not isinstance(row, dict):
                continue
            fpp = self._parse_front_panel_port(row)
            if fpp != port:
                continue
            metrics = row.get('metrics') if isinstance(row.get('metrics'), dict) else {}
            return DriverResult(success=True, data={
                'port': port,
                'link_status': metrics.get('link_status'),
                'link_state': self._link_state(metrics),
                'fec_mode': metrics.get('fec_mode'),
                'link_speed': metrics.get('link_speed'),
            })
        return DriverResult(error=f'Port {port} not found in metrics')

    def query_metrics(self, payload: dict | None = None) -> DriverResult:
        return self._post('/metrics/operations/query', payload or {})

    def clear_metrics(self) -> DriverResult:
        return self._post('/metrics/operations/clear', {})

    def switchover(self, enable: bool = True) -> DriverResult:
        return self._post('/control/operations/switchover', {'enable': bool(enable)})

    def doc_urls(self) -> dict[str, str]:
        host = unbracket_host(self.ip)
        return {
            'ui': f'https://{host}/',
            'connect_redoc': f'https://{host}/uhd_connect/redoc.html',
            'connect_openapi': f'https://{host}{_OPENAPI_CONNECT}',
            'samples': f'https://{host}/samples.tar.gz',
            'ixiac_redoc': f'https://{host}/ixiac/redoc.html',
            'ixiac_openapi': f'https://{host}{_OPENAPI_IXIAC}',
        }

    @staticmethod
    def _parse_front_panel_port(entry: dict) -> int | None:
        meta = entry.get('meta') if isinstance(entry.get('meta'), dict) else {}
        fpp = meta.get('front_panel_port')
        if fpp is not None:
            try:
                return int(fpp)
            except (TypeError, ValueError):
                pass
        port_name = str(entry.get('port_name') or '')
        m = re.search(r'Port\s+(\d+)', port_name, re.I)
        if m:
            return int(m.group(1))
        m = re.search(r'/(\d+)$', port_name)
        if m:
            return int(m.group(1))
        return None

    @staticmethod
    def _link_state(metrics: dict) -> str:
        raw = str((metrics or {}).get('link_status') or '').lower()
        if raw in ('link_up', 'up'):
            return 'up'
        if raw in ('link_down', 'down'):
            return 'down'
        return raw or 'unknown'

    def get_ports(self) -> DriverResult:
        """Return normalized port rows from live metrics."""
        metrics_res = self.query_metrics()
        if not metrics_res.success:
            return metrics_res

        data = metrics_res.data if isinstance(metrics_res.data, dict) else {}
        port_metrics = data.get('port_metrics') if isinstance(data.get('port_metrics'), dict) else {}
        entries = port_metrics.get('metrics') if isinstance(port_metrics.get('metrics'), list) else []

        config_res = self.get_config()
        config = config_res.data if config_res.success and isinstance(config_res.data, dict) else {}
        configured_names = self._configured_port_names(config)

        ports: list[dict] = []
        seen: set[int] = set()
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            fpp = self._parse_front_panel_port(entry)
            if fpp is None:
                continue
            seen.add(fpp)
            metrics = entry.get('metrics') if isinstance(entry.get('metrics'), dict) else {}
            link_state = self._link_state(metrics)
            logical_name = configured_names.get(fpp, '')
            display = str(fpp)
            ports.append({
                'front_panel_port': fpp,
                'port_number': fpp,
                'card_number': 1,
                'port_display': display,
                'port_name': entry.get('port_name', f'Port {fpp}'),
                'logical_name': logical_name,
                'link_state': link_state,
                'owner': 'Free',
                'speed': '',
                'metrics': metrics,
            })

        ports.sort(key=lambda p: p['front_panel_port'])
        return DriverResult(success=True, data=ports)

    @staticmethod
    def _configured_port_names(config: dict) -> dict[int, str]:
        """Map front-panel integer -> configured logical port name from active config."""
        mapping: dict[int, str] = {}
        for item in config.get('front_panel_ports') or []:
            if not isinstance(item, dict):
                continue
            name = str(item.get('name') or '').strip()
            choice = item.get('choice')
            if choice == 'front_panel_port':
                fpp = item.get('front_panel_port') if isinstance(item.get('front_panel_port'), dict) else {}
                num = fpp.get('front_panel_port')
                if name and num is not None:
                    try:
                        mapping[int(num)] = name
                    except (TypeError, ValueError):
                        pass
            elif choice == 'port_group':
                fpp = item.get('front_panel_port') if isinstance(item.get('front_panel_port'), dict) else {}
                num = fpp.get('front_panel_port')
                if name and num is not None:
                    try:
                        mapping[int(num)] = name
                    except (TypeError, ValueError):
                        pass
        return mapping

    def summarize_port_health(self, ports: list[dict]) -> dict:
        up = sum(1 for p in ports if (p.get('link_state') or '').lower() == 'up')
        down = sum(1 for p in ports if (p.get('link_state') or '').lower() == 'down')
        return {
            'total_ports': len(ports),
            'ports_up': up,
            'ports_down': down,
            'ports_unknown': len(ports) - up - down,
        }

    def get_health(self) -> DriverResult:
        ports_res = self.get_ports()
        if not ports_res.success:
            return ports_res
        ports = ports_res.data if isinstance(ports_res.data, list) else []
        summary = self.summarize_port_health(ports)
        status = 'healthy'
        if summary['ports_down'] > summary['ports_up']:
            status = 'degraded'
        return DriverResult(success=True, data={
            'cluster_health': status,
            'ports': summary,
        })

    def link_check(self, port_name: str = '') -> DriverResult:
        ports_res = self.get_ports()
        if not ports_res.success:
            return ports_res
        ports = ports_res.data if isinstance(ports_res.data, list) else []
        target = (port_name or '').strip()
        if target:
            matched = [
                p for p in ports
                if str(p.get('port_display')) == target
                or str(p.get('front_panel_port')) == target
                or str(p.get('logical_name') or '') == target
                or str(p.get('port_name') or '') == target
            ]
            if not matched:
                return DriverResult(error=f'Port not found: {port_name}')
            ports = matched
        rows = []
        for p in ports:
            link = (p.get('link_state') or 'unknown').lower()
            rows.append({
                'port': p.get('port_display'),
                'port_name': p.get('port_name'),
                'logical_name': p.get('logical_name') or '',
                'link_state': link,
                'link_up': link == 'up',
            })
        return DriverResult(success=True, data={'links': rows})
