"""
IxOS REST API Driver for Keysight / Ixia chassis.

Authentication : POST /platform/api/v1/auth/session  -> apiKey
Base URL       : https://{ip}/chassis/api/v2/ixos

Self-contained port of Labvault ixos.py for Velocity (no Django/labvault deps).

Author: rakesh.kumar@keysight.com
Written and debugged by rakesh.kumar@keysight.com
Co-authored-by: Cursor
"""
from __future__ import annotations

import ipaddress
import logging
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)


def bracket_host(host: str) -> str:
    """Bracket IPv6 literals for URL/host headers; leave IPv4/FQDN unchanged."""
    raw = (host or '').strip()
    if not raw:
        return ''
    if raw.startswith('['):
        return raw
    try:
        addr = ipaddress.ip_address(raw)
        if isinstance(addr, ipaddress.IPv6Address):
            return f'[{addr.compressed}]'
    except ValueError:
        pass
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


_api_key_cache: dict[str, str] = {}
_session_pool: dict[str, requests.Session] = {}


def _get_session(ip: str) -> requests.Session:
    if ip not in _session_pool:
        s = requests.Session()
        s.verify = False
        _session_pool[ip] = s
    return _session_pool[ip]


def fill_inferred_pcpu_mgmt_ips(ports: list[dict]) -> list[dict]:
    """Fill missing per-port PCPU management IPs from a validated card pattern."""
    by_card: dict[Any, list] = defaultdict(list)
    for p in ports:
        if isinstance(p, dict):
            by_card[p.get('card_number')].append(p)

    for card, plist in by_card.items():
        if card is None:
            continue
        try:
            card_i = int(card)
        except (TypeError, ValueError):
            continue
        confirmed = []
        for p in plist:
            ip = (p.get('management_ip') or '').strip()
            pn = p.get('port_number')
            if ip and pn is not None:
                confirmed.append((pn, ip))
        if not confirmed:
            continue
        if not all(ip == f'10.0.{card_i}.{pn}' for pn, ip in confirmed):
            continue
        for p in plist:
            pn = p.get('port_number')
            if pn is None:
                continue
            if not (p.get('management_ip') or '').strip():
                p['management_ip'] = f'10.0.{card_i}.{pn}'
                p['management_ip_inferred'] = True
    return ports


class IxOSDriver:
    """Driver for a single IxOS chassis."""

    def __init__(
        self,
        ip: str,
        username: str = 'admin',
        password: str = 'admin',
        *,
        hostname: str = '',
        chassis_type: str = '',
    ):
        self._host_raw = (ip or '').strip()
        self.ip = bracket_host(self._host_raw)
        self.username = username
        self.password = password
        self.hostname = (hostname or '').strip()
        self.chassis_type = (chassis_type or '').lower().replace('-', '').replace('_', '')
        self.api_key: str | None = _api_key_cache.get(self.ip)
        self._auth_uri = '/platform/api/v1/auth/session'
        self._last_ssh_error: str = ''

    def _ssh_hosts(self) -> list[str]:
        out: list[str] = []
        for h in (self.hostname, unbracket_host(self._host_raw)):
            h = (h or '').strip()
            if h and h not in out:
                out.append(h)
        return out

    def _needs_chassis_cli_prefix(self) -> bool:
        return self.chassis_type in ('xgs12', 'xgs2', 'xm', 'xg', 'ixvm')

    def _base_url(self):
        return f'https://{self.ip}/chassis/api/v2/ixos'

    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key or '',
        }

    def _authenticate(self) -> bool:
        session = _get_session(self.ip)
        url = f'https://{self.ip}{self._auth_uri}'
        payload = {
            'username': self.username,
            'password': self.password,
            'rememberMe': False,
            'resetWeakPassword': False,
        }
        try:
            resp = session.post(
                url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                verify=False,
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                self.api_key = data.get('apiKey', '')
                if self.api_key:
                    _api_key_cache[self.ip] = self.api_key
                    return True
            logger.debug('IxOS auth failed for %s: HTTP %s', self.ip, resp.status_code)
            return False
        except Exception as e:
            logger.debug('IxOS auth error for %s: %s', self.ip, e)
            return False

    def _ensure_auth(self) -> bool:
        if self.api_key:
            return True
        return self._authenticate()

    def _request(self, method: str, path: str, payload=None, timeout=12):
        if not self._ensure_auth():
            return None, None

        session = _get_session(self.ip)
        url = path if path.startswith('http') else self._base_url() + path

        for attempt in range(2):
            try:
                resp = session.request(
                    method,
                    url,
                    json=payload,
                    headers=self._headers(),
                    verify=False,
                    timeout=timeout,
                )

                if resp.status_code == 401 and attempt == 0:
                    self.api_key = None
                    _api_key_cache.pop(self.ip, None)
                    if self._authenticate():
                        continue
                    return None, None

                data = None
                try:
                    data = resp.json() if resp.text else None
                except Exception:
                    data = resp.text

                return resp, data
            except Exception as e:
                logger.debug('IxOS request error %s %s: %s', method, url, e)
                return None, None
        return None, None

    def _get(self, path: str, params=None, timeout=12):
        if not self._ensure_auth():
            return DriverResult(error='Authentication failed')
        session = _get_session(self.ip)
        url = path if path.startswith('http') else self._base_url() + path
        try:
            resp = session.get(
                url,
                params=params,
                headers=self._headers(),
                verify=False,
                timeout=timeout,
            )
            if resp.status_code == 401:
                self.api_key = None
                _api_key_cache.pop(self.ip, None)
                if self._authenticate():
                    resp = session.get(
                        url,
                        params=params,
                        headers=self._headers(),
                        verify=False,
                        timeout=timeout,
                    )
            if resp.status_code == 200:
                data = resp.json() if resp.text else None
                return DriverResult(success=True, data=data)
            return DriverResult(error=f'HTTP {resp.status_code}')
        except Exception as e:
            return DriverResult(error=str(e))

    def _post_operation(self, path: str, timeout=60):
        resp, data = self._request('POST', path, timeout=timeout)
        if resp is None:
            return DriverResult(error='Request failed')
        if resp.status_code == 200:
            return DriverResult(success=True, data=data)
        if resp.status_code == 202:
            return self._poll_async(data, timeout)
        return DriverResult(error=f'HTTP {resp.status_code}: {data}')

    def _poll_async(self, response_body, timeout=120):
        if not response_body or not isinstance(response_body, dict):
            return DriverResult(error='Invalid async response')
        poll_url = response_body.get('url', '')
        if not poll_url:
            return DriverResult(error='No poll URL in async response')
        start = time.time()
        while time.time() - start < timeout:
            time.sleep(2)
            resp, data = self._request('GET', poll_url)
            if resp is None:
                continue
            state = data.get('state', '') if isinstance(data, dict) else ''
            if state in ('SUCCESS', 'COMPLETED'):
                result_url = data.get('resultUrl', '')
                if result_url:
                    _r2, d2 = self._request('GET', result_url)
                    return DriverResult(success=True, data=d2)
                return DriverResult(success=True, data=data)
            if state == 'ERROR':
                return DriverResult(error=data.get('message', 'Async operation failed'))
        return DriverResult(error='Async operation timed out')

    def probe(self) -> str:
        try:
            if self._authenticate():
                result = self._get('/chassis', timeout=8)
                if result.success:
                    return 'ok'
                return 'ok'
            return 'auth_failed'
        except Exception:
            return 'unreachable'

    def get_chassis_info(self) -> DriverResult:
        result = self._get('/chassis')
        raw = None
        chassis_type = ''
        if result.success and result.data:
            raw = result.data
            if isinstance(raw, list) and raw:
                raw = raw[0]
            if isinstance(raw, dict):
                chassis_type = (raw.get('type') or '').strip()

        if not chassis_type or 'aresone' not in chassis_type.lower():
            platform_type = self._fetch_platform_chassis_type()
            if platform_type:
                chassis_type = platform_type
                logger.debug(
                    'IxOS %s: using Platform API chassis type %r',
                    self.ip,
                    chassis_type,
                )

        if not raw and not chassis_type:
            return result if not result.success else DriverResult(error='No chassis data')

        if not isinstance(raw, dict):
            raw = {}

        apps = {}
        for app in raw.get('ixosApplications', []):
            apps[app.get('name', '')] = app.get('version', '')

        info = {
            'management_ip': raw.get('managementIp', self.ip),
            'chassis_type': (chassis_type or raw.get('type', '')).replace(' ', '_'),
            'serial_number': raw.get('serialNumber', ''),
            'controller_serial': raw.get('controllerSerialNumber', ''),
            'state': raw.get('state', 'unknown'),
            'num_physical_cards': raw.get('numberOfPhysicalCards', 0),
            'ixos_applications': apps,
        }
        for name, ver in apps.items():
            if 'IxOS' in name:
                info['ixos_version'] = ver
                break
        return DriverResult(success=True, data=info)

    def _fetch_platform_chassis_type(self) -> str:
        if not self._ensure_auth():
            return ''
        url = f'https://{self.ip}/platform/api/v1/chassis'
        session = _get_session(self.ip)
        try:
            resp = session.get(
                url,
                headers=self._headers(),
                verify=False,
                timeout=12,
            )
            if resp.status_code != 200:
                return ''
            data = resp.json()
            if isinstance(data, list) and data:
                data = data[0]
            if isinstance(data, dict):
                return (data.get('type') or '').strip()
        except Exception as e:
            logger.debug('IxOS Platform API chassis type fetch %s: %s', self.ip, e)
        return ''

    def get_cards(self) -> DriverResult:
        result = self._get('/cards')
        if not result.success:
            return result
        raw = result.data if isinstance(result.data, list) else []
        cards = []
        for c in sorted(raw, key=lambda x: x.get('cardNumber', 999)):
            cards.append({
                'id': c.get('id', 0),
                'card_number': c.get('cardNumber', 0),
                'type': c.get('type', 'Unknown'),
                'state': c.get('state', 'unknown'),
                'serial_number': c.get('serialNumber', ''),
                'num_ports': c.get('numberOfPorts', 0),
            })
        return DriverResult(success=True, data=cards)

    @staticmethod
    def _port_display_name(raw: dict) -> str:
        fqn = (raw.get('fullyQualifiedPortName') or '').strip()
        if fqn and fqn.upper() != 'N/A':
            return fqn
        pn = raw.get('portNumber')
        try:
            pn_int = int(pn) if pn is not None else None
        except (TypeError, ValueError):
            pn_int = None
        if pn_int is not None and 9 <= pn_int <= 24:
            rg = (pn_int - 9) // 2 + 1
            sub = (pn_int - 9) % 2 + 1
            return f'{rg}.{sub}'
        cn = raw.get('cardNumber', 0)
        return f'{cn}.{pn_int}' if pn_int is not None else str(cn)

    def get_ports(self) -> DriverResult:
        result = self._get('/ports')
        if not result.success:
            return result
        raw = result.data if isinstance(result.data, list) else []
        ports = []
        for p in raw:
            owner = p.get('owner', '') or 'Free'
            link_state_raw = p.get('linkState', 'unknown')
            link_state, led_color = self._normalize_link(link_state_raw, owner)
            port_memory_raw = p.get('portMemory')
            port_memory_kb = None
            if port_memory_raw is not None:
                try:
                    port_memory_kb = float(port_memory_raw)
                except (TypeError, ValueError):
                    port_memory_kb = None
            port_row = {
                'id': p.get('id', 0),
                'card_number': p.get('cardNumber', 0),
                'port_number': p.get('portNumber', 0),
                'owner': owner,
                'link_state': link_state,
                'link_state_raw': link_state_raw,
                'led_color': led_color,
                'speed': p.get('speed', ''),
                'phy_mode': p.get('phyMode', ''),
                'transmit_state': p.get('transmitState', ''),
                'transceiver_model': p.get('transceiverModel', ''),
                'transceiver_mfg': p.get('transceiverManufacturer', ''),
                'type': p.get('type', ''),
                'pcpu_status': p.get('pcpuStatus', ''),
                'port_memory_kb': port_memory_kb,
                'fully_qualified_port_name': (p.get('fullyQualifiedPortName') or '').strip(),
                'management_ip': (p.get('managementIp') or '').strip(),
                'port_display': self._port_display_name(p),
            }
            rgn = p.get('resourceGroupNumber', p.get('resourceGroupId'))
            rg_obj = p.get('resourceGroup')
            if rgn is None and isinstance(rg_obj, dict):
                rgn = rg_obj.get('number', rg_obj.get('id', rg_obj.get('resourceGroupNumber')))
            elif rgn is None and rg_obj is not None:
                rgn = rg_obj
            if rgn is not None:
                try:
                    port_row['resource_group_number'] = int(rgn)
                except (TypeError, ValueError):
                    pass
            ports.append(port_row)
        fill_inferred_pcpu_mgmt_ips(ports)
        ports.sort(key=lambda x: (x['card_number'], x['port_number']))
        return DriverResult(success=True, data=ports)

    def get_lldp_peers(self) -> DriverResult:
        if not self._ensure_auth():
            return DriverResult(error='Authentication failed')

        for path in (
            '/lldpneighbors',
            '/lldppeers',
            '/lldpNeighbors',
            '/lldp/neighbors',
            '/neighbors/lldp',
        ):
            r = self._get(path, timeout=12)
            if r.success and r.data:
                parsed = self._parse_lldp_payload(r.data)
                if parsed:
                    return DriverResult(success=True, data=parsed)

        r = self._get('/ports', timeout=18)
        if r.success and isinstance(r.data, list):
            parsed = self._parse_lldp_from_ports(r.data)
            if parsed:
                return DriverResult(success=True, data=parsed)

        return DriverResult(success=True, data=[])

    def _parse_lldp_payload(self, data):
        if isinstance(data, list):
            return self._normalize_lldp_rows(data)
        if not isinstance(data, dict):
            return []
        for key in ('lldpNeighbors', 'neighbors', 'lldp', 'items', 'data', 'ports'):
            inner = data.get(key)
            if isinstance(inner, list):
                parsed = self._normalize_lldp_rows(inner)
                if parsed:
                    return parsed
        return []

    def _normalize_lldp_rows(self, rows):
        out = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            lp = r.get('localPort', r.get('local_port', ''))
            if isinstance(lp, (int, float)):
                lp = str(int(lp))
            rem = (
                r.get('systemName')
                or r.get('system_name')
                or r.get('remoteSystemName')
                or r.get('remote_device')
                or ''
            )
            rport = (
                r.get('portId')
                or r.get('port_id')
                or r.get('remotePortId')
                or r.get('remote_port')
                or ''
            )
            if isinstance(rport, dict):
                rport = rport.get('id', '') or rport.get('name', '')
            cid = r.get('chassisId') or r.get('chassis_id') or ''
            mgmt = (
                r.get('managementAddress')
                or r.get('managementIp')
                or r.get('mgmt_ip')
                or ''
            )
            if rem or rport or cid:
                out.append({
                    'local_port': str(lp).strip(),
                    'remote_device': str(rem).strip(),
                    'remote_port': str(rport).strip(),
                    'chassis_id': str(cid).strip(),
                    'mgmt_ip': str(mgmt).strip() if mgmt else '',
                })
        return out

    def _parse_lldp_from_ports(self, raw_ports):
        out = []
        for p in raw_ports:
            if not isinstance(p, dict):
                continue
            peer = None
            for k in ('lldpNeighbor', 'lldpNeighborInfo', 'lldpPeer', 'lldp', 'neighbor'):
                v = p.get(k)
                if isinstance(v, dict) and (
                    v.get('systemName')
                    or v.get('system_name')
                    or v.get('remoteSystemName')
                ):
                    peer = v
                    break
            if not peer:
                continue
            cn = int(p.get('cardNumber', p.get('card_number', 0)) or 0)
            pn = p.get('portNumber', p.get('port_number'))
            try:
                pn = int(pn) if pn is not None else None
            except (TypeError, ValueError):
                pn = None

            if pn is not None and 9 <= pn <= 24:
                rg = (pn - 9) // 2 + 1
                sub = (pn - 9) % 2 + 1
                local_port = f'{rg}.{sub}'
            elif cn is not None and pn is not None:
                local_port = f'{cn}.{pn}'
            else:
                local_port = str(pn or '')

            rem = (
                peer.get('systemName')
                or peer.get('system_name')
                or peer.get('remoteSystemName')
                or ''
            )
            rport = (
                peer.get('portId')
                or peer.get('port_id')
                or peer.get('portDescription')
                or peer.get('remotePortId')
                or ''
            )
            if isinstance(rport, dict):
                rport = rport.get('id', '') or rport.get('name', '')
            mgmt = (
                peer.get('managementAddress')
                or peer.get('managementIp')
                or peer.get('mgmtIp')
                or ''
            )
            out.append({
                'local_port': local_port,
                'remote_device': str(rem).strip(),
                'remote_port': str(rport).strip(),
                'chassis_id': str(peer.get('chassisId') or peer.get('chassis_id') or '').strip(),
                'mgmt_ip': str(mgmt).strip() if mgmt else '',
            })
        return out

    def _ssh_run(self, cmd: str, timeout: int = 12) -> str:
        self._last_ssh_error = ''
        base_cmd = (cmd or '').strip()
        if not base_cmd:
            return ''

        if self._needs_chassis_cli_prefix() and not base_cmd.lower().startswith('chassis '):
            commands = [f'chassis {base_cmd}', base_cmd]
        else:
            commands = [base_cmd]
            if not self._needs_chassis_cli_prefix():
                commands.append(f'chassis {base_cmd}')

        for host in self._ssh_hosts():
            try:
                import paramiko
            except ImportError:
                self._last_ssh_error = 'paramiko not installed on execution agent'
                return ''
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(
                    host,
                    username=self.username,
                    password=self.password,
                    timeout=8,
                    look_for_keys=False,
                    allow_agent=False,
                )
                last_out = ''
                for run_cmd in commands:
                    _, stdout, _ = client.exec_command(run_cmd, timeout=timeout)
                    last_out = stdout.read().decode('utf-8', errors='replace')
                    if last_out and 'Unknown or incomplete command' not in last_out:
                        return last_out
                if last_out:
                    return last_out
            except Exception as e:
                self._last_ssh_error = f'{host}: {e}'
                logger.debug('IxOS SSH %s cmd=%r failed: %s', host, base_cmd, e)
            finally:
                try:
                    client.close()
                except Exception:
                    pass
        return ''

    def get_topology_ssh(self) -> DriverResult:
        raw = self._ssh_run('show topology', timeout=12)
        if not raw or 'Card' not in raw:
            return DriverResult(error='show topology returned no data')
        topo = self._parse_show_topology(raw)
        if not topo.get('cards'):
            return DriverResult(error='No cards parsed from show topology')
        return DriverResult(success=True, data=topo)

    def _parse_show_topology(self, output: str) -> dict:
        cards: dict[int, dict] = {}
        cli_ports_by_card: dict[int, list[str]] = {}
        current_card: int | None = None
        current_rg: dict | None = None

        for line in output.splitlines():
            stripped = line.lstrip(' |`+-\t')

            card_m = re.match(
                r'Card\s+(\d+)\s+(.*?)(?:\s*\(SN\s+(\S+)\))?\s*$',
                stripped,
            )
            if card_m:
                current_card = int(card_m.group(1))
                cards[current_card] = {
                    'description': card_m.group(2).strip(),
                    'serial': (card_m.group(3) or '').strip(),
                    'resource_groups': [],
                }
                cli_ports_by_card[current_card] = []
                current_rg = None
                continue

            rg_m = re.match(
                r'Resource Group\s+(\d+)\s+\(RG(\d+)\)-?\s*(.*?)(?:\s+mode)?\s*$',
                stripped,
            )
            if not rg_m:
                rg_m = re.match(
                    r'Resource Group\s+(\d+)\s*(?:\(RG\d+\))?\s*-?\s*(.*?)(?:\s+mode)?\s*$',
                    stripped,
                )
            if rg_m and current_card is not None:
                rg_num = int(rg_m.group(1))
                if rg_m.lastindex and rg_m.lastindex >= 3:
                    mode_str = (rg_m.group(3) or '').strip()
                else:
                    mode_str = (rg_m.group(2) or '').strip()
                current_rg = {
                    'number': rg_num,
                    'label': f'RG{rg_num:02d}',
                    'mode': mode_str,
                    'ports': [],
                }
                cards[current_card]['resource_groups'].append(current_rg)
                continue

            port_m = re.match(
                r'Port\s+([\d.]+)\s+(.+?)\s+Link\s+(\S+)',
                stripped,
            )
            if port_m and current_card is not None:
                display = port_m.group(1)
                middle = port_m.group(2).strip()
                link = port_m.group(3)
                owner_m = re.search(r'\(([^)]*)\)\s*$', middle)
                if owner_m:
                    owner = owner_m.group(1)
                    ptype = middle[: owner_m.start()].strip()
                else:
                    owner = ''
                    ptype = middle
                entry = {
                    'display': display,
                    'type': ptype,
                    'owner': owner,
                    'link': link,
                }
                if current_rg is not None:
                    current_rg['ports'].append(entry)
                cli_ports_by_card[current_card].append(display)
                continue

            port_loose = re.match(r'Port\s+([\d.]+)\s+(.+)$', stripped)
            if port_loose and current_card is not None:
                display = port_loose.group(1)
                rest = port_loose.group(2).strip()
                link_m = re.search(r'Link\s*:\s*(\S+)|\bLink\s+(\S+)', rest)
                link = (link_m.group(1) or link_m.group(2)) if link_m else ''
                owner_m = re.search(r'\(([^)]*)\)\s*$', rest)
                if owner_m:
                    owner = owner_m.group(1)
                    ptype = rest[: owner_m.start()].strip()
                else:
                    owner = ''
                    ptype = rest
                entry = {
                    'display': display,
                    'type': ptype,
                    'owner': owner,
                    'link': link or 'unknown',
                }
                if current_rg is not None:
                    current_rg['ports'].append(entry)
                cli_ports_by_card[current_card].append(display)

        for c_num, card_info in cards.items():
            if card_info.get('resource_groups'):
                continue
            displays = cli_ports_by_card.get(c_num) or []
            if not displays:
                continue
            card_info['resource_groups'] = [{
                'number': 1,
                'label': 'RG01',
                'mode': '',
                'ports': [
                    {'display': d, 'type': '', 'owner': '', 'link': ''}
                    for d in displays
                ],
            }]

        return {
            'cards': cards,
            'cli_ports_by_card': cli_ports_by_card,
        }

    def correlate_ports(self, topo_data: dict, rest_ports: list) -> dict:
        api_by_card: dict[int, list[int]] = defaultdict(list)
        for p in rest_ports:
            api_by_card[p.get('card_number', 0)].append(p.get('port_number', 0))
        for v in api_by_card.values():
            v.sort()

        cli_by_card = topo_data.get('cli_ports_by_card', {})
        mapping: dict[tuple[int, int], str] = {}

        for card_num, api_ports in api_by_card.items():
            cli_ports = cli_by_card.get(card_num, [])
            if len(api_ports) == len(cli_ports):
                for api_pn, cli_display in zip(api_ports, cli_ports):
                    mapping[(card_num, api_pn)] = cli_display
            else:
                for api_pn in api_ports:
                    mapping[(card_num, api_pn)] = str(api_pn)

        return mapping

    def get_lldp_ssh(
        self,
        bps_topology: dict | None = None,
        chassis_type: str = '',
    ) -> DriverResult:
        raw = self._ssh_run('show lldp-peer-info data', timeout=12)
        if not raw:
            return DriverResult(error='SSH lldp-peer-info returned no data')
        neighbors = self._parse_lldp_peer_info(raw)
        return DriverResult(success=True, data=neighbors)

    @staticmethod
    def _parse_lldp_peer_info(output: str) -> list[dict]:
        neighbors: list[dict] = []
        current: dict | None = None

        for line in output.splitlines():
            stripped = line.strip()
            if not stripped or stripped.lower().startswith('chassis peer'):
                continue
            port_m = re.match(r'^Port\s+([\d.]+)\s*$', stripped, re.I)
            card_port_m = re.match(r'^Card\s+(\d+)\s+Port\s+(\d+)\s*$', stripped, re.I)
            if port_m or card_port_m:
                if current and current.get('local_port'):
                    neighbors.append(current)
                if card_port_m:
                    cn, pn = card_port_m.group(1), card_port_m.group(2)
                    local_port = f'{cn}/{pn}'
                else:
                    local_port = port_m.group(1)
                current = {
                    'local_port': local_port,
                    'remote_device': '',
                    'remote_port': '',
                    'chassis_id': '',
                    'mgmt_ip': '',
                }
                continue
            if current is None:
                continue
            if ':' not in stripped:
                continue
            key, _, val = stripped.partition(':')
            key = key.strip().lower()
            val = val.strip()
            if key == 'system name':
                current['remote_device'] = val
            elif key == 'system ip':
                current['mgmt_ip'] = val
            elif key == 'system mac':
                current['chassis_id'] = val
            elif key == 'port id':
                current['remote_port'] = val
            elif key == 'port description':
                if not current['remote_port'] or current['remote_port'].startswith('Eth'):
                    current['remote_port'] = val

        if current and current.get('local_port') and (
            current.get('remote_device') or current.get('mgmt_ip')
        ):
            neighbors.append(current)

        return neighbors

    def take_ownership(self, port_id: int) -> DriverResult:
        return self._post_operation(f'/ports/{port_id}/operations/takeownership')

    def release_ownership(self, port_id: int) -> DriverResult:
        return self._post_operation(f'/ports/{port_id}/operations/releaseownership')

    def reboot_port(self, port_id: int) -> DriverResult:
        return self._post_operation(f'/ports/{port_id}/operations/reboot')

    @staticmethod
    def _normalize_link(raw_state: str, owner: str = '') -> tuple[str, str]:
        low = raw_state.lower()
        if low in ('linkup', 'up'):
            return 'up', 'green'
        if low in ('linkdown', 'down'):
            if owner and owner != 'Free':
                return 'down', 'yellow'
            return 'down', 'red'
        if low in ('notransceiver', 'no_transceiver'):
            return 'noTransceiver', 'off'
        if low in ('loopback',):
            return 'loopback', 'amber'
        if low in ('admindisabled', 'disabled'):
            return 'disabled', 'yellow'
        return raw_state, 'off'

    def get_health(self) -> DriverResult:
        """Chassis controller CPU/memory from /perfcounters (latest sample)."""
        result = self._get('/perfcounters')
        empty = {
            'cpu_utilization': 0,
            'memory_used': 0,
            'memory_total': 0,
            'disk_io_bps': 0,
        }
        if not result.success:
            return DriverResult(success=True, data=empty)
        raw = result.data
        if isinstance(raw, list):
            rows = [r for r in raw if isinstance(r, dict)]
            if not rows:
                return DriverResult(success=True, data=empty)
            raw = max(rows, key=lambda r: r.get('sequence', 0))
        if not isinstance(raw, dict):
            return DriverResult(success=True, data=empty)
        return DriverResult(success=True, data={
            'cpu_utilization': raw.get('cpuUsagePercent', 0),
            'memory_used': int(raw.get('memoryInUseBytes', 0) or 0),
            'memory_total': int(raw.get('memoryTotalBytes', 0) or 0),
            'disk_io_bps': float(raw.get('diskIOBytesPerSecond', 0) or 0),
        })

    def get_sensors(self) -> DriverResult:
        """Temperature / fan / voltage sensors when exposed by REST."""
        for path in ('/sensors', '/environment', '/chassis/sensors'):
            result = self._get(path)
            if result.success and result.data:
                return result
        return DriverResult(success=True, data=[])

    def summarize_port_health(self, ports: list[dict]) -> dict:
        """Aggregate link/owner stats for reservation healthcheck."""
        total = len(ports)
        up = sum(1 for p in ports if (p.get('link_state') or '').lower() == 'up')
        owned = sum(1 for p in ports if (p.get('owner') or 'Free') not in ('', 'Free'))
        no_xcvr = sum(
            1 for p in ports
            if 'notransceiver' in (p.get('link_state') or '').lower()
            or 'notransceiver' in (p.get('link_state_raw') or '').lower()
        )
        return {
            'total_ports': total,
            'ports_up': up,
            'ports_down': total - up,
            'ports_owned': owned,
            'ports_no_transceiver': no_xcvr,
        }
