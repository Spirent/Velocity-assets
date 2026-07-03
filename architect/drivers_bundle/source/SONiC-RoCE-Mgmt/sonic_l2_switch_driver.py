"""
Spirent Velocity - SONiC NOS Layer 2 Switch Driver
===================================================
Version  : 1.0.0
Interface: Layer 2 Switch (Velocity standard)
Supports : Any switch running SONiC open-source NOS
           Tested platforms: Arista (SONiC build), Nvidia Spectrum (SONiC build)

Driver entry point defined in manifest.xml ? entryPoint.

Layer 2 Switch interface methods (required by Velocity):
    getProperties, getPorts, createVlan, destroyVlan, addToVlan, removeFromVlan

Lifecycle methods (called by Velocity topology Setup / Teardown actions):
    setup, teardown, verifyReady

Port control:
    setSpeed, setAdminState

Monitoring:
    healthcheck, getLldpNeighbors

Admin / one-time:
    createBaseline, listBaselines, runCommand

Pre-Load Strategy (see Appendix C of LaaS Implementation Plan):
    Layer 1 - Golden Config JSON per speed template (baseline_*.json)
    Layer 2 - SONiC native checkpoint / rollback  (SONiC 202205+)
    Layer 3 - In-session state tracking for fast incremental teardown

Author : rakesh.kumar@keysight.com
Written and debugged by rakesh.kumar@keysight.com
Co-authored-by: Cursor
Date   : 2026-06-18
"""

import os
import re
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    import paramiko
except ImportError:
    raise ImportError(
        "paramiko is required: pip install paramiko\n"
        "Install on the Velocity agent host, not the switch."
    )

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
log = logging.getLogger("sonic_driver")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# ---------------------------------------------------------------------------
# Speed constants - SONiC uses Mbps integers for 'config interface speed'
# ---------------------------------------------------------------------------
SPEED_MAP = {
    10:    10000,
    25:    25000,
    40:    40000,
    50:    50000,
    100:   100000,
    200:   200000,
    400:   400000,
    800:   800000,
}

# Reverse map: SONiC output strings ? canonical Gbps int
SPEED_STR_TO_GBPS = {
    "10G":   10,  "10000":  10,
    "25G":   25,  "25000":  25,
    "40G":   40,  "40000":  40,
    "50G":   50,  "50000":  50,
    "100G": 100,  "100000": 100,
    "200G": 200,  "200000": 200,
    "400G": 400,  "400000": 400,
    "800G": 800,  "800000": 800,
}

# Default baseline filename template
BASELINE_FILENAME = "baseline_{speed}G.json"
BASELINE_DEFAULT  = "baseline_default.json"

ANSI_ESCAPE = re.compile(r"\[[0-9;]*[A-Za-z]")


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub("", text or "")


def parse_bool_option(value, default=False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def velocity_error(message: str, **extra) -> dict:
    out = {"status": "error", "error": message}
    out.update(extra)
    return out


def safe_driver_method(fn):
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except Exception as exc:
            log.exception("[%s] %s failed", getattr(self, "host", "?"), fn.__name__)
            return velocity_error(str(exc), method=fn.__name__)
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


# ===========================================================================
# SSH Session Helper
# ===========================================================================
class SonicSSH:
    """
    Thin wrapper around Paramiko for SONiC CLI interaction.

    SONiC drops the user into a standard Linux bash shell as 'admin'.
    All 'config' and most 'show' commands require sudo (passwordless by default).
    """

    PROMPT = re.compile(r"[\w.\-@]+[:#$]\s*$", re.MULTILINE)

    def __init__(self, host: str, username: str, password: str,
                 port: int = 22, connect_timeout: int = 30,
                 command_timeout: int = 60, sudo_password: str = ""):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connect_timeout = connect_timeout
        self.command_timeout = command_timeout
        self.sudo_password = sudo_password
        self._client: Optional[paramiko.SSHClient] = None
        self._shell: Optional[paramiko.Channel] = None

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------
    def connect(self):
        log.info("Connecting to %s:%d as %s", self.host, self.port, self.username)
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cred_pairs = [
            (self.username, self.password),
            ("admin", "password"),
            ("admin", "YourPaSsWoRd"),
        ]
        seen = set()
        last_err = None
        for user, pwd in cred_pairs:
            key = (user, pwd)
            if key in seen or not user:
                continue
            seen.add(key)
            try:
                self._client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=user,
                    password=pwd,
                    timeout=self.connect_timeout,
                    look_for_keys=False,
                    allow_agent=False,
                )
                self.username = user
                self.password = pwd
                break
            except Exception as exc:
                last_err = exc
                self._client = paramiko.SSHClient()
                self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            raise ConnectionError(f"SSH connect failed to {self.host}: {last_err}")
        self._shell = self._client.invoke_shell(width=220, height=50)
        self._shell.settimeout(self.command_timeout)
        self._drain()          # consume login banner
        log.info("Connected to %s", self.host)

    def disconnect(self):
        if self._shell:
            self._shell.close()
        if self._client:
            self._client.close()
        log.info("Disconnected from %s", self.host)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_):
        self.disconnect()

    # ------------------------------------------------------------------
    # Command execution
    # ------------------------------------------------------------------
    def run(self, cmd: str, timeout: Optional[int] = None) -> str:
        """Execute a single command and return its output (stripped)."""
        timeout = timeout or self.command_timeout
        log.debug("run(%s): %s", self.host, cmd)
        self._shell.send(cmd + "\n")
        return self._collect(timeout)

    def sudo(self, cmd: str, timeout: Optional[int] = None) -> str:
        """Run a command with sudo, handling password prompt if needed."""
        full_cmd = f"sudo {cmd}"
        self._shell.send(full_cmd + "\n")
        output = self._collect(timeout or self.command_timeout, extra_prompt=r"\[sudo\] password")
        if "[sudo] password" in output and self.sudo_password:
            self._shell.send(self.sudo_password + "\n")
            output += self._collect(timeout or self.command_timeout)
        return output

    def vtysh(self, vtysh_cmd: str) -> str:
        """Run a command inside vtysh (FRR shell for BGP/routing state)."""
        return self.sudo(f'vtysh -c "{vtysh_cmd}"')

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _drain(self, wait: float = 2.0) -> str:
        time.sleep(wait)
        buf = ""
        while self._shell.recv_ready():
            buf += self._shell.recv(65535).decode("utf-8", errors="replace")
        return buf

    def _collect(self, timeout: int, extra_prompt: str = "") -> str:
        """Read from shell until prompt (or extra_prompt) is detected."""
        buf = ""
        deadline = time.time() + timeout
        prompt_re = re.compile(
            extra_prompt + r"|" + self.PROMPT.pattern if extra_prompt
            else self.PROMPT.pattern,
            re.MULTILINE,
        )
        while time.time() < deadline:
            if self._shell.recv_ready():
                chunk = self._shell.recv(65535).decode("utf-8", errors="replace")
                buf += chunk
                if prompt_re.search(buf):
                    break
            else:
                time.sleep(0.1)
        return self._strip_prompt(buf)

    @staticmethod
    def _strip_prompt(text: str) -> str:
        """Remove the trailing shell prompt from output."""
        lines = text.splitlines()
        while lines and re.search(r"[\w.\-@]+[:#$]\s*$", lines[-1]):
            lines.pop()
        return "\n".join(lines).strip()


# ===========================================================================
# SONiC Output Parsers
# ===========================================================================
class SonicParser:
    """Static parsers for SONiC CLI output."""

    # ------------------------------------------------------------------
    # 'show interfaces status'
    # ------------------------------------------------------------------
    @staticmethod
    def parse_interfaces(raw: str) -> list[dict]:
        """Parse ``show interfaces status`` with header-relative column detection."""
        raw = strip_ansi(raw)
        lines = [ln for ln in raw.splitlines() if ln.strip()]
        header_idx = next(
            (i for i, ln in enumerate(lines) if "Interface" in ln and "Speed" in ln),
            None,
        )
        if header_idx is None:
            return []
        header = re.split(r"\s{2,}", lines[header_idx].strip())
        col = {name.lower(): idx for idx, name in enumerate(header)}

        def col_val(parts, *names, default="unknown"):
            for name in names:
                idx = col.get(name.lower())
                if idx is not None and idx < len(parts):
                    return parts[idx]
            return default

        ports = []
        for line in lines[header_idx + 1 :]:
            if line.strip().startswith("-") or not line.strip():
                continue
            parts = re.split(r"\s{2,}", line.strip())
            if not parts:
                continue
            iface = parts[0]
            if not iface.startswith("Ethernet"):
                continue
            speed_str = col_val(parts, "speed", default="N/A")
            oper = col_val(parts, "oper", "oper state", default="unknown")
            admin = col_val(parts, "admin", "admin state", default="unknown")
            vlan_info = col_val(parts, "vlan", "vlan(s)", default="routed")
            status = "online" if str(oper).lower() in ("up", "connected") else "offline"
            ports.append({
                "name": iface,
                "status": status,
                "speed_str": speed_str,
                "speed_gbps": SPEED_STR_TO_GBPS.get(str(speed_str).upper(), 0),
                "oper_state": oper,
                "admin_state": admin,
                "vlan": vlan_info,
            })
        return ports

    # ------------------------------------------------------------------
    # 'show vlan brief'
    # ------------------------------------------------------------------
    @staticmethod
    def parse_vlans(raw: str) -> list[dict]:
        """
        Parse 'show vlan brief' output.

        Returns list of: {vlan_id, ports: [{name, tagging}]}
        """
        vlans = []
        current = None
        for line in raw.splitlines():
            # Table row with VLAN ID (pipe-delimited)
            m = re.match(r"\|\s+(\d+)\s+\|.*\|\s*(.*?)\s*\|\s*(.*?)\s*\|", line)
            if m:
                vlan_id   = int(m.group(1))
                port_name = m.group(2).strip()
                tagging   = m.group(3).strip()
                current = {"vlan_id": vlan_id, "ports": []}
                if port_name:
                    current["ports"].append({"name": port_name, "tagging": tagging})
                vlans.append(current)
            elif current and re.match(r"\|\s*\|.*\|\s*(Ethernet\S+)\s*\|\s*(.*?)\s*\|", line):
                # Continuation row - additional ports for same VLAN
                cm = re.match(r"\|\s*\|.*\|\s*(Ethernet\S+)\s*\|\s*(.*?)\s*\|", line)
                if cm:
                    current["ports"].append({
                        "name": cm.group(1).strip(),
                        "tagging": cm.group(2).strip(),
                    })
        return vlans

    # ------------------------------------------------------------------
    # 'show version'
    # ------------------------------------------------------------------
    @staticmethod
    def parse_version(raw: str) -> dict:
        """Extract SONiC version, OS version, platform, and hostname."""
        info = {}
        patterns = {
            "sonic_version": r"SONiC Software Version:\s*SONiC\.(.+)",
            "os_version":    r"OS Version:\s*(.+)",
            "platform":      r"Platform:\s*(.+)",
            "hwsku":         r"HwSKU:\s*(.+)",
            "asic":          r"ASIC vendor:\s*(.+)",
            "hostname":      r"Hostname:\s*(.+)",
            "uptime":        r"Uptime:\s*(.+)",
        }
        for key, pattern in patterns.items():
            m = re.search(pattern, raw, re.IGNORECASE)
            info[key] = m.group(1).strip() if m else "unknown"
        return info

    @staticmethod
    def parse_bgp_summary(raw: str) -> dict:
        """Parse ``show bgp summary`` / vtysh output."""
        raw = strip_ansi(raw)
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
        peers = []
        for line in lines:
            low = line.lower()
            if low.startswith('neighbor') or line.startswith('=') or 'received prefixes' in low:
                continue
            parts = line.split()
            if len(parts) >= 2 and ('.' in parts[0] or ':' in parts[0]):
                peers.append({
                    'neighbor': parts[0],
                    'asn': parts[1] if len(parts) > 1 else '',
                    'state': parts[-1] if parts else '',
                    'raw': line,
                })
        return {'peer_count': len(peers), 'peers': peers[:64]}

    # ------------------------------------------------------------------
    # 'show lldp neighbors'
    # ------------------------------------------------------------------

    @staticmethod
    def parse_lldp_table(raw: str) -> list[dict]:
        """Parse ``show lldp table`` style output."""
        raw = strip_ansi(raw)
        if not raw or ("LocalPort" not in raw and "Local Port" not in raw):
            return []
        lines = raw.strip().splitlines()
        header_idx = next(
            (i for i, ln in enumerate(lines) if "LocalPort" in ln or "Local Port" in ln),
            0,
        )
        out = []
        for line in lines[header_idx + 1 :]:
            stripped = line.strip()
            if not stripped or stripped.startswith("---"):
                continue
            low = stripped.lower()
            if "total entries displayed" in low or low.startswith("total "):
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            loc, rem, rport = parts[0], parts[1], parts[2]
            if loc in ("LocalPort", "Local", "Port") or rem in ("--------------", "Capability"):
                continue
            out.append({
                "local_port": loc,
                "remote_host": rem,
                "remote_port": rport,
                "description": " ".join(parts[3:]) if len(parts) > 3 else "",
            })
        return out

    @staticmethod
    def parse_lldp(raw: str) -> list[dict]:
        """Parse LLDP neighbor table into list of neighbor dicts."""
        neighbors = []
        for line in raw.splitlines():
            # Format: LocalPort  RemoteDevice  RemotePortID  RemotePortDescription
            parts = line.split()
            if len(parts) >= 3 and parts[0].startswith("Ethernet"):
                neighbors.append({
                    "local_port":   parts[0],
                    "remote_host":  parts[1],
                    "remote_port":  parts[2],
                    "description":  " ".join(parts[3:]) if len(parts) > 3 else "",
                })
        return neighbors


# ===========================================================================
# Main Driver Class
# ===========================================================================
class SonicL2SwitchDriver:
    """
    Spirent Velocity Layer 2 Switch driver for SONiC NOS.

    Velocity calls driver methods via the entry point defined in manifest.xml.
    Properties (host, username, password, etc.) are injected by Velocity
    from the resource inventory at instantiation time.

    Session state tracking (Layer 3 teardown):
        self._session tracks every config change made during a reservation
        so teardown can perform a fast incremental undo before the
        checkpoint rollback (Layer 2).
    """

    def __init__(self, resource_properties: dict):
        """
        Called by Velocity when a resource is first accessed.

        resource_properties keys (from manifest.xml <properties>):
            host, username, password, port, baselines_path,
            connect_timeout, command_timeout, reload_timeout,
            verify_timeout, checkpoint_name, use_checkpoint, sudo_password
        """
        self.host             = resource_properties.get("host", "")
        self.username         = resource_properties.get("username", "admin")
        self.password         = resource_properties.get("password", "")
        self.port             = int(resource_properties.get("port", 22))
        self.baselines_path   = resource_properties.get("baselines_path", "/etc/sonic/baselines")
        self.connect_timeout  = int(resource_properties.get("connect_timeout", 30))
        self.command_timeout  = int(resource_properties.get("command_timeout", 60))
        self.reload_timeout   = int(resource_properties.get("reload_timeout", 180))
        self.verify_timeout   = int(resource_properties.get("verify_timeout", 120))
        self.checkpoint_name  = resource_properties.get("checkpoint_name", "velocity_pre_reservation")
        self.use_checkpoint   = parse_bool_option(resource_properties.get("use_checkpoint"), True)
        self.sudo_password    = resource_properties.get("sudo_password", "")
        self.allow_missing_baseline = parse_bool_option(
            resource_properties.get("allow_missing_baseline"), False
        )
        self.allow_run_command = parse_bool_option(
            resource_properties.get("allow_run_command"), False
        )
        self.allow_sudo_run_command = parse_bool_option(
            resource_properties.get("allow_sudo_run_command"), False
        )
        self.reservation_id = resource_properties.get("reservation_id", "") or os.environ.get(
            "VELOCITY_PARAM_RESERVATION_ID", ""
        )
        self.default_speed_gbps = int(
            resource_properties.get("defaultSpeedGbps")
            or resource_properties.get("default_speed_gbps")
            or 400
        )
        self.default_template = str(
            resource_properties.get("defaultTemplate")
            or resource_properties.get("default_template")
            or "RoCE-400G"
        )
        self.port_aliases = self._load_aliases(resource_properties)
        self._state_dir = Path(
            resource_properties.get(
                "state_dir",
                os.environ.get("VELOCITY_DRIVER_STATE_DIR", "/tmp/velocity_sonic_state"),
            )
        )
        self._state_file = self._state_dir / f"{self.host.replace(':', '_')}_{self.reservation_id or 'default'}.json"

        self._ssh: Optional[SonicSSH] = None
        self._load_persistent_state()
        if not self._session.get("start_time"):
            self._reset_session_state()

    # ------------------------------------------------------------------
    # Internal session state (Layer 3 tracking)
    # ------------------------------------------------------------------
    def _reset_session_state(self):
        self._session = {
            "vlans_created":  [],    # [vlan_id, ...]
            "ports_modified": [],    # [(port, original_speed_mbps), ...]
            "ports_in_vlan":  [],    # [(vlan_id, port, mode), ...]  mode=tagged|untagged
            "ports_shutdown": [],    # [port, ...]  admin shutdown during session
            "reservation_id": None,
            "template":       None,
            "speed_gbps":     None,
            "start_time":     None,
        }

    def _load_aliases(self, props: dict) -> dict:
        aliases = {}
        raw = props.get("port_aliases") or props.get("portAliases") or ""
        if raw:
            try:
                data = json.loads(raw) if isinstance(raw, str) else raw
                if isinstance(data, dict):
                    aliases = {str(k): str(v) for k, v in data.items()}
            except Exception:
                log.warning("Invalid port_aliases JSON; ignoring")
        path = props.get("port_aliases_file") or props.get("portAliasesFile")
        if path and Path(path).is_file():
            try:
                data = json.loads(Path(path).read_text())
                if isinstance(data, dict):
                    aliases.update({str(k): str(v) for k, v in data.items()})
            except Exception as exc:
                log.warning("Could not read port_aliases_file %s: %s", path, exc)
        if not aliases:
            bundled = Path(__file__).resolve().parent / "sonic_port_aliases.json"
            if bundled.is_file():
                try:
                    data = json.loads(bundled.read_text())
                    if isinstance(data, dict):
                        aliases.update({str(k): str(v) for k, v in data.items()})
                except Exception as exc:
                    log.warning("Could not read bundled sonic_port_aliases.json: %s", exc)
        return aliases

    def _resolve_port(self, port: str) -> str:
        if not port:
            return port
        return self.port_aliases.get(port, self.port_aliases.get(port.lower(), port))

    def _load_persistent_state(self):
        self._reset_session_state()
        try:
            if self._state_file.is_file():
                data = json.loads(self._state_file.read_text())
                if isinstance(data, dict):
                    self._session.update(data)
        except Exception as exc:
            log.warning("Could not load persistent state %s: %s", self._state_file, exc)

    def _save_persistent_state(self):
        try:
            self._state_dir.mkdir(parents=True, exist_ok=True)
            self._state_file.write_text(json.dumps(self._session, indent=2))
        except Exception as exc:
            log.warning("Could not save persistent state %s: %s", self._state_file, exc)


    # ------------------------------------------------------------------
    # SSH connection helpers
    # ------------------------------------------------------------------
    def _connect(self) -> SonicSSH:
        if self._ssh is None:
            self._ssh = SonicSSH(
                host=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                connect_timeout=self.connect_timeout,
                command_timeout=self.command_timeout,
                sudo_password=self.sudo_password,
            )
            self._ssh.connect()
        return self._ssh

    def _disconnect(self):
        if self._ssh:
            self._ssh.disconnect()
            self._ssh = None

    def _run(self, cmd: str, timeout: int = None) -> str:
        return self._connect().run(cmd, timeout)

    def _sudo(self, cmd: str, timeout: int = None) -> str:
        return self._connect().sudo(cmd, timeout)

    def _collect_ports(self) -> list:
        raw = self._run("show interfaces status")
        ports = SonicParser.parse_interfaces(raw)
        vlan_raw = self._run("show vlan brief")
        vlans = SonicParser.parse_vlans(vlan_raw)
        vlan_by_port = {}
        for v in vlans:
            for p in v["ports"]:
                vlan_by_port.setdefault(p["name"], []).append(
                    f"vlan{v['vlan_id']}({p['tagging']})"
                )
        for port in ports:
            port["vlan_membership"] = ", ".join(vlan_by_port.get(port["name"], ["none"]))
        return ports

    # ==================================================================
    # VELOCITY INTERFACE: getProperties
    # ==================================================================
    def getProperties(self, args=None) -> dict:
        """Return Velocity property inventory; optional -includePorts true."""
        log.info("[%s] getProperties", self.host)
        raw = self._run("show version")
        info = SonicParser.parse_version(raw)
        include_ports = False
        if args:
            for i, token in enumerate(args):
                if token in ("-includePorts", "-includeports") and i + 1 < len(args):
                    include_ports = parse_bool_option(args[i + 1], False)

        properties = {
            "Hostname": info.get("hostname", self.host),
            "Make": "SONiC",
            "Model": info.get("hwsku", info.get("platform", "unknown")),
            "SerialNumber": "N/A",
            "SonicVersion": info.get("sonic_version", "unknown"),
            "OsVersion": info.get("os_version", "unknown"),
            "Asic": info.get("asic", "unknown"),
            "Uptime": info.get("uptime", "unknown"),
            "ManagementIPv4": self.host,
            "DriverVersion": "1.0.0",
        }
        result = {"properties": properties}
        if include_ports:
            result["ports"] = self._collect_ports()
        return result

    # ==================================================================
    # VELOCITY INTERFACE: getPorts
    # ==================================================================
    def getPorts(self, args=None) -> dict:
        """Return Velocity port inventory JSON."""
        log.info("[%s] getPorts", self.host)
        raw = self._run("show interfaces status")
        ports = SonicParser.parse_interfaces(raw)

        vlan_raw = self._run("show vlan brief")
        vlans = SonicParser.parse_vlans(vlan_raw)
        vlan_by_port = {}
        for v in vlans:
            for p in v["ports"]:
                vlan_by_port.setdefault(p["name"], []).append(
                    f"vlan{v['vlan_id']}({p['tagging']})"
                )

        velocity_ports = []
        for port in ports:
            internal = port["name"]
            display = self.port_aliases.get(internal, internal)
            for alias, target in self.port_aliases.items():
                if target == internal and alias != internal:
                    display = alias
                    break
            velocity_ports.append({
                "name": display,
                "status": port.get("status", "offline"),
                "container": port.get("speed_str", ""),
            })

        log.info("[%s] Found %d ports", self.host, len(velocity_ports))
        return {"ports": velocity_ports}

    # ==================================================================
    # VELOCITY INTERFACE: createVlan
    # ==================================================================
    def createVlan(self, args=None) -> dict:
        """
        Create a VLAN on the switch.

        Args:
            vlan_id: VLAN ID (1-4094)

        Returns:
            dict with status and vlan_id
        """
        if not args:
            return velocity_error("createVlan requires vlanId")
        vlan_id = int(args[0])
        log.info("[%s] createVlan %d", self.host, vlan_id)
        self._validate_vlan_id(vlan_id)

        out = self._sudo(f"config vlan add {vlan_id}")
        if "Error" in out or "error" in out:
            raise RuntimeError(f"createVlan({vlan_id}) failed: {out}")

        self._session["vlans_created"].append(vlan_id)
        log.info("[%s] VLAN %d created", self.host, vlan_id)
        self._save_persistent_state()
        return {"status": "ok", "vlan_id": vlan_id}

    # ==================================================================
    # VELOCITY INTERFACE: destroyVlan
    # ==================================================================
    def destroyVlan(self, args=None) -> dict:
        """
        Remove a VLAN from the switch.

        All ports must be removed from the VLAN before calling this.
        Velocity calls removeFromVlan first as part of topology cleanup.

        Args:
            vlan_id: VLAN ID to remove
        """
        if not args:
            return velocity_error("destroyVlan requires vlanId")
        vlan_id = int(args[0])
        log.info("[%s] destroyVlan %d", self.host, vlan_id)

        out = self._sudo(f"config vlan del {vlan_id}")
        if "Error" in out or "error" in out:
            log.warning("[%s] destroyVlan(%d) warning: %s", self.host, vlan_id, out)

        # Remove from session tracking
        if vlan_id in self._session["vlans_created"]:
            self._session["vlans_created"].remove(vlan_id)

        return {"status": "ok", "vlan_id": vlan_id}

    # ==================================================================
    # VELOCITY INTERFACE: addToVlan
    # ==================================================================
    def addToVlan(self, args=None) -> dict:
        """
        Add a port to a VLAN.

        Args:
            port:    Interface name (e.g., "Ethernet0")
            vlan_id: VLAN ID
            mode:    "tagged" (trunk) or "untagged" (access)

        SONiC syntax:
            tagged:   config vlan member add <id> <port>
            untagged: config vlan member add <id> <port> -u
        """
        if not args or len(args) < 2:
            return velocity_error("addToVlan requires vlanId portNumber [tagging]")
        vlan_id = int(args[0])
        port = self._resolve_port(str(args[1]))
        mode = (args[2] if len(args) > 2 else "tagged").lower()
        log.info("[%s] addToVlan port=%s vlan=%d mode=%s", self.host, port, vlan_id, mode)
        self._validate_port(port)
        self._validate_vlan_id(vlan_id)

        flag = "-u" if mode == "untagged" else ""
        out = self._sudo(f"config vlan member add {vlan_id} {port} {flag}".strip())
        if "Error" in out or "error" in out:
            raise RuntimeError(f"addToVlan({port}, {vlan_id}, {mode}) failed: {out}")

        self._session["ports_in_vlan"].append((vlan_id, port, mode))
        self._save_persistent_state()
        return {"status": "ok", "port": port, "vlan_id": vlan_id, "mode": mode}

    # ==================================================================
    # VELOCITY INTERFACE: removeFromVlan
    # ==================================================================
    def removeFromVlan(self, args=None) -> dict:
        """
        Remove a port from a VLAN.

        Args:
            port:    Interface name
            vlan_id: VLAN ID
        """
        if not args or len(args) < 2:
            return velocity_error("removeFromVlan requires vlanId portNumber")
        vlan_id = int(args[0])
        port = self._resolve_port(str(args[1]))
        log.info("[%s] removeFromVlan port=%s vlan=%d", self.host, port, vlan_id)

        out = self._sudo(f"config vlan member del {vlan_id} {port}")
        if "Error" in out or "error" in out:
            log.warning("[%s] removeFromVlan warning: %s", self.host, out)

        # Remove from session tracking
        self._session["ports_in_vlan"] = [
            e for e in self._session["ports_in_vlan"]
            if not (e[0] == vlan_id and e[1] == port)
        ]
        self._save_persistent_state()
        return {"status": "ok", "port": port, "vlan_id": vlan_id}

    # ==================================================================
    # LIFECYCLE: setup
    # ==================================================================
    def setup(self, args=None) -> dict:
        args = args or []
        if len(args) >= 2:
            template = args[0]
            speed_gbps = int(args[1])
            reservation_id = args[2] if len(args) > 2 else self.reservation_id
        else:
            template = self.default_template
            speed_gbps = self.default_speed_gbps
            reservation_id = self.reservation_id
        start = time.time()
        log.info("[%s] setup: template=%s speed=%dG reservation=%s",
                 self.host, template, speed_gbps, reservation_id)

        self._reset_session_state()
        self._session.update({
            "reservation_id": reservation_id,
            "template":       template,
            "speed_gbps":     speed_gbps,
            "start_time":     datetime.utcnow().isoformat(),
        })

        # --- Layer 1: Load baseline config ---
        baseline_file = f"{self.baselines_path}/{BASELINE_FILENAME.format(speed=speed_gbps)}"
        log.info("[%s] Loading baseline: %s", self.host, baseline_file)
        self._load_baseline(baseline_file)

        # --- Layer 2: Create checkpoint (SONiC 202205+) ---
        if self.use_checkpoint:
            log.info("[%s] Creating checkpoint: %s", self.host, self.checkpoint_name)
            self._create_checkpoint()

        # --- Verify all ports UP ---
        ready = self.verifyReady([str(speed_gbps)])

        elapsed = round(time.time() - start, 1)
        log.info("[%s] setup complete in %ss", self.host, elapsed)
        status = "ready"
        if isinstance(ready, dict) and ready.get("status") != "all_up":
            status = "degraded"
        return {
            "status":       status,
            "host":         self.host,
            "template":     template,
            "speed_gbps":   speed_gbps,
            "baseline":     baseline_file,
            "setup_time_s": elapsed,
            "verifyReady":  ready if isinstance(ready, dict) else {},
        }

    # ==================================================================
    # LIFECYCLE: teardown
    # ==================================================================
    def teardown(self, args=None) -> dict:
        """
        Reservation teardown action - called by Velocity at reservation end.

        Implements the three-layer cleanup in reverse order:
          Layer 3: Incremental undo of session changes (fast, seconds)
          Layer 2: Checkpoint rollback to post-baseline state
          Layer 1: Fallback - reload default baseline if rollback unavailable

        Returns:
            dict with status and teardown duration
        """
        start = time.time()
        log.info("[%s] teardown: reservation=%s", self.host,
                 self._session.get("reservation_id", "unknown"))

        errors = []

        # --- Layer 3: Incremental undo ---
        try:
            self._incremental_undo()
        except Exception as e:
            log.warning("[%s] Incremental undo partial failure: %s", self.host, e)
            errors.append(f"incremental_undo: {e}")

        # --- Layer 2: Checkpoint rollback ---
        if self.use_checkpoint:
            try:
                self._rollback_checkpoint()
            except Exception as e:
                log.warning("[%s] Checkpoint rollback failed, falling back to config reload: %s",
                            self.host, e)
                errors.append(f"checkpoint_rollback: {e}")
                # Layer 1 fallback
                try:
                    self._load_baseline(
                        f"{self.baselines_path}/{BASELINE_DEFAULT}",
                        reload=True
                    )
                except Exception as e2:
                    errors.append(f"fallback_reload: {e2}")
        else:
            # Layer 1 only (older SONiC)
            try:
                self._load_baseline(
                    f"{self.baselines_path}/{BASELINE_DEFAULT}",
                    reload=True
                )
            except Exception as e:
                errors.append(f"default_reload: {e}")

        self._disconnect()
        self._reset_session_state()

        elapsed = round(time.time() - start, 1)
        log.info("[%s] teardown complete in %ss", self.host, elapsed)
        return {
            "status":        "released" if not errors else "released_with_warnings",
            "host":          self.host,
            "teardown_time_s": elapsed,
            "warnings":      errors,
        }

    # ==================================================================
    # LIFECYCLE: verifyReady
    # ==================================================================
    def verifyReady(self, args=None) -> dict:
        expected_speed_gbps = int(args[0]) if args else None
        """
        Poll 'show interfaces status' until all Ethernet ports are operationally UP.

        Called after setup() completes baseline load. Returns when all ports
        are UP or raises TimeoutError if verify_timeout is exceeded.

        Args:
            expected_speed_gbps: If set, also verify all ports are at this speed.

        Returns:
            dict with all_up status, port count, elapsed time
        """
        log.info("[%s] verifyReady: expected_speed=%sG timeout=%ds",
                 self.host, expected_speed_gbps or "any", self.verify_timeout)
        deadline = time.time() + self.verify_timeout
        poll_interval = 5

        while time.time() < deadline:
            raw = self._run("show interfaces status")
            ports = SonicParser.parse_interfaces(raw)
            ethernet_ports = [p for p in ports if p["name"].startswith("Ethernet")]

            if not ethernet_ports:
                time.sleep(poll_interval)
                continue

            down_ports = [p for p in ethernet_ports if p["oper_state"].lower() != "up"]
            wrong_speed = []
            if expected_speed_gbps:
                wrong_speed = [
                    p for p in ethernet_ports
                    if p["speed_gbps"] != 0 and p["speed_gbps"] != expected_speed_gbps
                ]

            if not down_ports and not wrong_speed:
                log.info("[%s] All %d ports UP at %sG",
                         self.host, len(ethernet_ports), expected_speed_gbps or "expected")
                return {
                    "status":      "all_up",
                    "port_count":  len(ethernet_ports),
                    "elapsed_s":   round(self.verify_timeout - (deadline - time.time()), 1),
                }

            log.debug("[%s] Waiting: %d down, %d wrong speed",
                      self.host, len(down_ports), len(wrong_speed))
            time.sleep(poll_interval)

        return {
            "status": "timeout",
            "port_count": len(ethernet_ports) if ethernet_ports else 0,
            "down_ports": [p["name"] for p in down_ports],
            "wrong_speed": [p["name"] for p in wrong_speed],
            "verify_timeout_s": self.verify_timeout,
        }

    def setConfig(self, args=None) -> dict:
        """CONFIGURABLE — load speed baseline (ignores Velocity config asset URL)."""
        return self.setup()

    def getConfig(self, args=None) -> dict:
        raw = self._run("show runningconfiguration all")
        return {"status": "ok", "config_preview": raw[:2000] if raw else ""}

    # ==================================================================
    # PORT CONTROL: setSpeed
    # ==================================================================
    def setSpeed(self, args=None) -> dict:
        if not args or len(args) < 2:
            return velocity_error("setSpeed requires port speedGbps")
        port = self._resolve_port(str(args[0]))
        speed_gbps = int(args[1])
        log.info("[%s] setSpeed %s ? %dG", self.host, port, speed_gbps)
        self._validate_port(port)

        if speed_gbps not in SPEED_MAP:
            raise ValueError(f"Unsupported speed: {speed_gbps}G. Valid: {list(SPEED_MAP)}")

        # Record original speed for teardown
        raw = self._run(f"show interfaces status {port}")
        ports = SonicParser.parse_interfaces(raw)
        original_mbps = SPEED_MAP.get(ports[0]["speed_gbps"], 0) if ports else 0

        speed_mbps = SPEED_MAP[speed_gbps]
        out = self._sudo(f"config interface speed {port} {speed_mbps}")
        if "Error" in out or "error" in out:
            raise RuntimeError(f"setSpeed({port}, {speed_gbps}G) failed: {out}")

        self._session["ports_modified"].append((port, original_mbps))
        log.info("[%s] %s speed set to %dG (%d Mbps)", self.host, port, speed_gbps, speed_mbps)
        return {"status": "ok", "port": port, "speed_gbps": speed_gbps}

    # ==================================================================
    # PORT CONTROL: setAdminState
    # ==================================================================
    def setAdminState(self, args=None) -> dict:
        if not args or len(args) < 2:
            return velocity_error("setAdminState requires port state")
        port = self._resolve_port(str(args[0]))
        state = str(args[1]).lower()
        log.info("[%s] setAdminState %s ? %s", self.host, port, state)
        self._validate_port(port)

        if state == "up":
            cmd = f"config interface startup {port}"
        elif state in ("down", "shutdown"):
            cmd = f"config interface shutdown {port}"
            self._session["ports_shutdown"].append(port)
        else:
            raise ValueError(f"Invalid state '{state}'. Use 'up' or 'down'.")

        out = self._sudo(cmd)
        if "Error" in out or "error" in out:
            raise RuntimeError(f"setAdminState({port}, {state}) failed: {out}")

        return {"status": "ok", "port": port, "admin_state": state}

    # ==================================================================
    # MONITORING: healthcheck
    # ==================================================================
    def healthcheck(self, args=None) -> dict:
        """
        Check that all ports are still UP. Called by Velocity every 15 minutes
        during an active reservation.

        Returns:
            dict with overall health, per-port status, and any failures.
            Velocity alerts the reservation owner if 'health' != 'ok'.
        """
        log.info("[%s] healthcheck", self.host)
        raw = self._run("show interfaces status")
        ports = SonicParser.parse_interfaces(raw)
        ethernet = [p for p in ports if p["name"].startswith("Ethernet")]

        down = [p for p in ethernet if p["oper_state"].lower() != "up"]
        health = "ok" if not down else "degraded"

        if down:
            log.warning("[%s] HEALTH: %d ports DOWN: %s",
                        self.host, len(down), [p["name"] for p in down])

        lldp_count = 0
        try:
            neighbors = self.getLldpNeighbors()
            lldp_count = len(neighbors.get("neighbors") or [])
        except Exception as exc:
            log.warning("[%s] healthcheck LLDP probe failed: %s", self.host, exc)

        return {
            "health":        health,
            "host":          self.host,
            "total_ports":   len(ethernet),
            "up_ports":      len(ethernet) - len(down),
            "down_ports":    [{"name": p["name"], "speed": p["speed_str"]} for p in down],
            "lldp_neighbors": lldp_count,
            "checked_at":    datetime.utcnow().isoformat() + "Z",
        }

    # ==================================================================
    # MONITORING: getLldpNeighbors
    # ==================================================================
    @safe_driver_method
    def getLldpNeighbors(self, args=None) -> dict:
        """
        Return LLDP neighbor table for OCS / fabric validation.
        """
        log.info("[%s] getLldpNeighbors", self.host)
        raw = self._run("show lldp neighbors")
        neighbors = SonicParser.parse_lldp_table(raw) or SonicParser.parse_lldp(raw)
        log.info("[%s] Found %d LLDP neighbors", self.host, len(neighbors))
        return {"neighbors": neighbors}

    @safe_driver_method
    def getBgpSummary(self, args=None) -> dict:
        """BGP summary for CLOS spine validation (FRR/vtysh)."""
        log.info("[%s] getBgpSummary", self.host)
        try:
            raw = self._connect().vtysh("show bgp summary")
        except Exception:
            raw = self._sudo("vtysh -c 'show bgp summary'")
        summary = SonicParser.parse_bgp_summary(raw)
        summary["host"] = self.host
        return summary

    # ==================================================================
    # ADMIN: createBaseline
    # ==================================================================
    def createBaseline(self, args=None) -> dict:
        if not args:
            return velocity_error("createBaseline requires name")
        name = args[0]
        """
        Save the current running config as a named baseline JSON file.

        Called once by a lab admin after configuring the switch to a known
        good state for a given speed template. The saved file is then used
        by setup() for future reservations.

        Args:
            name: Baseline name, e.g., "baseline_800G" (no .json extension needed)

        SONiC command: sudo config save -y  (saves to /etc/sonic/config_db.json)
        Then copies to baselines directory.
        """
        log.info("[%s] createBaseline: %s", self.host, name)
        if not name.endswith(".json"):
            name = name + ".json"

        dest = f"{self.baselines_path}/{name}"
        out = self._sudo(f"mkdir -p {self.baselines_path}")
        out = self._sudo(f"config save -y")      # writes /etc/sonic/config_db.json
        out = self._sudo(f"cp /etc/sonic/config_db.json {dest}")
        if "No such file" in out or "Permission denied" in out:
            raise RuntimeError(f"createBaseline failed: {out}")

        log.info("[%s] Baseline saved to %s", self.host, dest)
        return {"status": "ok", "path": dest, "created_at": datetime.utcnow().isoformat()}

    # ==================================================================
    # ADMIN: listBaselines
    # ==================================================================
    def listBaselines(self) -> list[str]:
        """
        Return list of available baseline JSON files on the switch.
        """
        log.info("[%s] listBaselines from %s", self.host, self.baselines_path)
        out = self._run(f"ls {self.baselines_path}/*.json 2>/dev/null")
        files = [f.strip() for f in out.splitlines() if f.strip().endswith(".json")]
        return files

    # ==================================================================
    # ADMIN: runCommand
    # ==================================================================
    def runCommand(self, cmd: str, use_sudo: bool = False,
                   timeout: int = None) -> str:
        """
        Execute an arbitrary SONiC CLI command and return raw output.

        Used for diagnostics, custom show commands, or one-off config
        not covered by the standard interface methods.

        Args:
            cmd:      Command string (do not include 'sudo' prefix)
            use_sudo: If True, prepend sudo
            timeout:  Override default command timeout (seconds)
        """
        log.info("[%s] runCommand (sudo=%s): %s", self.host, use_sudo, cmd)
        if use_sudo:
            return self._sudo(cmd, timeout=timeout)
        return self._run(cmd, timeout=timeout)

    # ==================================================================
    # PRIVATE: Pre-load Layer 1 - baseline config load
    # ==================================================================
    def _load_baseline(self, baseline_file: str, reload: bool = True):
        """Load a baseline JSON config and optionally trigger config reload."""
        log.info("[%s] Loading baseline config: %s", self.host, baseline_file)

        # Check file exists
        check = self._run(f"test -f {baseline_file} && echo EXISTS || echo MISSING")
        if "MISSING" in check:
            if self.allow_missing_baseline:
                log.warning("[%s] Baseline missing (allowed): %s", self.host, baseline_file)
                return
            raise FileNotFoundError(
                f"Baseline not found on switch: {baseline_file}. "
                "Run createBaseline() or set allow_missing_baseline=true for lab use."
            )

        # Load into config DB
        out = self._sudo(f"config load {baseline_file} -y",
                         timeout=self.command_timeout)
        if "Error" in out or "error" in out.lower():
            raise RuntimeError(f"config load failed: {out}")

        if reload:
            log.info("[%s] config reload (ASIC reprogramming, allow %ds)",
                     self.host, self.reload_timeout)
            out = self._sudo("config reload -y", timeout=self.reload_timeout)
            if "Error" in out or "error" in out.lower():
                raise RuntimeError(f"config reload failed: {out}")
            # Brief wait for ASIC to settle
            time.sleep(5)

    # ==================================================================
    # PRIVATE: Pre-load Layer 2 - checkpoint management
    # ==================================================================
    def _create_checkpoint(self):
        """Create a SONiC config checkpoint (requires SONiC 202205+)."""
        out = self._sudo(f"config checkpoint {self.checkpoint_name}",
                         timeout=self.command_timeout)
        if "Error" in out or "error" in out.lower():
            raise RuntimeError(f"config checkpoint failed: {out}")
        log.info("[%s] Checkpoint '%s' created", self.host, self.checkpoint_name)

    def _rollback_checkpoint(self):
        """Roll back to the stored checkpoint (SONiC 202205+)."""
        log.info("[%s] Rolling back to checkpoint: %s", self.host, self.checkpoint_name)
        out = self._sudo(f"config rollback {self.checkpoint_name} -y",
                         timeout=self.reload_timeout)
        if "Error" in out or "error" in out.lower():
            raise RuntimeError(f"config rollback failed: {out}")
        time.sleep(3)
        log.info("[%s] Rollback complete", self.host)

    # ==================================================================
    # PRIVATE: Pre-load Layer 3 - incremental undo
    # ==================================================================
    def _incremental_undo(self):
        """
        Undo session changes in reverse order (fast path before checkpoint rollback).

        Order:
          1. Remove ports from VLANs
          2. Delete VLANs created during session
          3. Restore port speeds
          4. Bring back up any admin-shutdown ports
        """
        log.info("[%s] Incremental undo: vlans=%d ports_in_vlan=%d speed_changes=%d",
                 self.host,
                 len(self._session["vlans_created"]),
                 len(self._session["ports_in_vlan"]),
                 len(self._session["ports_modified"]))

        # 1. Remove ports from VLANs (reverse order)
        for vlan_id, port, _ in reversed(self._session["ports_in_vlan"]):
            try:
                self._sudo(f"config vlan member del {vlan_id} {port}")
            except Exception as e:
                log.warning("[%s] undo removeFromVlan(%d, %s): %s", self.host, vlan_id, port, e)

        # 2. Delete VLANs (reverse order)
        for vlan_id in reversed(self._session["vlans_created"]):
            try:
                self._sudo(f"config vlan del {vlan_id}")
            except Exception as e:
                log.warning("[%s] undo destroyVlan(%d): %s", self.host, vlan_id, e)

        # 3. Restore port speeds
        for port, original_mbps in reversed(self._session["ports_modified"]):
            if original_mbps > 0:
                try:
                    self._sudo(f"config interface speed {port} {original_mbps}")
                except Exception as e:
                    log.warning("[%s] undo setSpeed(%s, %d): %s", self.host, port, original_mbps, e)

        # 4. Re-enable any shutdown ports
        for port in self._session["ports_shutdown"]:
            try:
                self._sudo(f"config interface startup {port}")
            except Exception as e:
                log.warning("[%s] undo shutdown(%s): %s", self.host, port, e)

    # ==================================================================
    # PRIVATE: Validators
    # ==================================================================
    @staticmethod
    def _validate_port(port: str):
        if not re.match(r"^Ethernet\d+$", port):
            raise ValueError(
                f"Invalid port name '{port}'. "
                "SONiC ports must be 'EthernetN' (e.g., Ethernet0, Ethernet4)."
            )

    @staticmethod
    def _validate_vlan_id(vlan_id: int):
        if not 1 <= vlan_id <= 4094:
            raise ValueError(f"VLAN ID {vlan_id} out of range (1-4094).")



# Velocity whitelist dispatch (no eval)
ALLOWED_CALLS = {
    "getProperties": "getProperties",
    "getPorts": "getPorts",
    "getVlans": "getVlans",
    "createVlan": "createVlan",
    "destroyVlan": "destroyVlan",
    "addToVlan": "addToVlan",
    "removeFromVlan": "removeFromVlan",
    "setup": "setup",
    "teardown": "teardown",
    "verifyReady": "verifyReady",
    "setSpeed": "setSpeed",
    "setAdminState": "setAdminState",
    "healthcheck": "healthcheck",
    "getLldpNeighbors": "getLldpNeighbors",
    "getBgpSummary": "getBgpSummary",
    "createBaseline": "createBaseline",
    "listBaselines": "listBaselines",
    "runCommand": "runCommand",
    "probe": "probe",
    "setConfig": "setConfig",
    "getConfig": "getConfig",
}


def _env_properties() -> dict:
    props = {}
    for key, val in os.environ.items():
        if key.startswith("VELOCITY_PARAM_property_"):
            props[key.replace("VELOCITY_PARAM_property_", "", 1)] = val
    props.setdefault("host", props.get("ipAddress", props.get("Hostname", "")))
    props.setdefault("username", props.get("username", "admin"))
    props.setdefault("password", props.get("password", ""))
    props.setdefault("port", props.get("SSH_Port", props.get("port", "22")))
    if "VELOCITY_PARAM_RESERVATION_ID" in os.environ:
        props["reservation_id"] = os.environ["VELOCITY_PARAM_RESERVATION_ID"]
    return props


def getVlans(self, args=None):
    """Return configured VLANs."""
    raw = self._run("show vlan brief")
    vlans = SonicParser.parse_vlans(raw)
    return {"vlans": vlans}


# attach getVlans to class
SonicL2SwitchDriver.getVlans = getVlans


def _run_velocity_dispatch():
    _driver = SonicL2SwitchDriver(_env_properties())
    try:
        for _call_number in range(int(os.environ["VELOCITY_PARAM_call_count"])):
            _env_var = os.environ.get(f"VELOCITY_PARAM_call_{_call_number}", "")
            _parts = _env_var.split()
            _call_name = _parts[0] if _parts else ""
            _call_args = _parts[1:] if len(_parts) > 1 else None

            _method_name = ALLOWED_CALLS.get(_call_name)
            if not _method_name:
                retVal = velocity_error(f"Unknown or disallowed call: {_call_name}")
            else:
                _method = getattr(_driver, _method_name)
                retVal = _method() if not _call_args else _method(_call_args)

            print(json.dumps(retVal))
    finally:
        _driver._disconnect()


if "VELOCITY_PARAM_call_count" in os.environ:
    _run_velocity_dispatch()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SONiC Velocity Driver - manual test")
    parser.add_argument("--host",     required=True,  help="Switch management IP")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="")
    parser.add_argument("--command",  default="getProperties",
                        help="Driver command to test")
    parser.add_argument("--params",   default="{}",
                        help="JSON params for command")
    args = parser.parse_args()

    props = {
        "host":     args.host,
        "username": args.username,
        "password": args.password,
    }
    params = json.loads(args.params)

    logging.basicConfig(level=logging.DEBUG)
    os.environ["VELOCITY_PARAM_call_count"] = "1"
    os.environ["VELOCITY_PARAM_call_0"] = args.command + (
        " " + " ".join(str(v) for v in params.values()) if params else ""
    )
    for k, v in props.items():
        os.environ[f"VELOCITY_PARAM_property_{k}"] = str(v)
    _run_velocity_dispatch()
    print(json.dumps(result, indent=2))
