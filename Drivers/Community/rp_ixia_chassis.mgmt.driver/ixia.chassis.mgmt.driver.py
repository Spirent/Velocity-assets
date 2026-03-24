import sys
import os
import paramiko
import time
import logging
import json
import re


# create logger and set debugging level
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)
# create console handler and set level
ch = logging.StreamHandler()
# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

COMMAND_TIMEOUT = 30


class IxiaChassis:
    def __init__(self, address, username, password, port=22):
        self.address = address
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(
            address,
            port=int(port),
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
        )
        self.shell = self.client.invoke_shell()
        # consume the login banner / initial prompt
        self._recv()

    def _recv(self):
        timeout = time.time() + COMMAND_TIMEOUT
        response = ""
        while True:
            time.sleep(0.1)
            if self.shell.recv_ready():
                chunk = self.shell.recv(65535).decode("utf-8", errors="replace")
                response += chunk
            if time.time() > timeout:
                break
            # stop when we see a shell prompt
            if re.search(r"[>#$]\s*$", response):
                break
        # strip ANSI escape codes
        response = re.sub(r"\x1b\[[0-9;]*[mGKHF]", "", response)
        logger.debug("Raw response: " + response)
        return response

    def _exec(self, command):
        self.shell.send(command + "\n")
        return self._recv()

    def getProperties(self, args=None):
        # use the connection IP as hostname — IxOS has no 'hostname' command
        hostname = self.address

        # parse '| Key : Value |' table from 'show welcome-screen'
        welcome_out = self._exec("show welcome-screen")
        mgmt_ipv4 = ""
        mgmt_ipv6 = ""
        ixos_version = ""
        ixnetwork_version = ""
        license_version = ""
        chassis_status = ""
        for line in welcome_out.splitlines():
            m = re.match(r"\|\s*(.+?)\s*:\s*(.+?)\s*\|", line)
            if m:
                key = m.group(1).strip().lower()
                val = m.group(2).strip()
                if "management ipv4" in key:
                    mgmt_ipv4 = val
                elif "management ipv6" in key:
                    mgmt_ipv6 = val
                elif "active ixos version" in key:
                    ixos_version = val
                elif "ixnetwork protocols version" in key:
                    ixnetwork_version = val
                elif "licenseserverplus version" in key:
                    license_version = val
                elif "chassis status" in key:
                    chassis_status = val

        # parse chassis model and serial from first line of 'show topology'
        # e.g. "AresONE - Primary (ChassisSN MY24310002)"
        topo_out = self._exec("show topology")
        chassis_model = ""
        chassis_serial = ""
        for line in topo_out.splitlines():
            m = re.match(r"^(.+?)\s+\(ChassisSN\s+(\S+)\)", line.strip())
            if m:
                chassis_model = m.group(1).strip()
                chassis_serial = m.group(2).strip()
                break

        resource_properties = {
            "Make": "Keysight",
            "Hostname": hostname,
            "Model": chassis_model,
            "Serial Number": chassis_serial,
            "ManagementIPv4": mgmt_ipv4,
            "ManagementIPv6": mgmt_ipv6,
            "IxOSVersion": ixos_version,
            "IxNetworkVersion": ixnetwork_version,
            "LicenseServerVersion": license_version,
            "ChassisStatus": chassis_status,
        }

        return_dict = {"properties": resource_properties}

        if args and args[0] == "true":
            port_list = self._parsePorts(topo_out)
            return_dict["ports"] = port_list["ports"]

        return return_dict

    def _parsePorts(self, output):
        port_list = []
        current_rg = "Card 1"
        for line in output.splitlines():
            stripped = line.strip()
            # track current Resource Group, e.g. "Resource Group 01 (RG01)-..."
            rg_m = re.search(r"Resource Group\s+\d+\s+\((\w+)\)", stripped)
            if rg_m:
                current_rg = rg_m.group(1)
                continue
            # match port lines, e.g.:
            # "+- Port 1.1 100GBASE-CR (IxNetwork/...) Link Up"
            # "+- Port 2.1 400GBASE-CR4 Link Down"
            port_m = re.search(
                r"Port\s+(\d+(?:\.\d+)?)\s+(\S+).*Link\s+(Up|Down)", stripped, re.IGNORECASE
            )
            if port_m:
                port_name = port_m.group(1)
                speed = port_m.group(2)
                status = port_m.group(3).lower()
                # speed_m = re.match(r"(\d+)", speed)
                # port_speed = int(speed_m.group(1)) if speed_m else 0
                port_properties = {
                    "name": port_name,
                    # "portNumber": speed,
                    # "Port Type": 'Fast Ethernet',
                    "status": status,
                    # "speed": speed,
                    # "Port Speed": port_speed * 1000,
                    "container": f"{current_rg} {speed}",
                }
                port_list.append(port_properties)
                logger.debug("Port: %s", port_properties)

        return {"ports": port_list}

    def getPorts(self, args=None):
        output = self._exec("show topology")
        return self._parsePorts(output)

    def runCommand(self, args=None):
        if not args:
            return {"output": "", "error": "No command specified"}
        command = " ".join(args)
        output = self._exec(command)
        # strip the echoed command and trailing prompt
        lines = output.splitlines()
        if len(lines) > 2:
            lines = lines[1:-1]
        return {"output": "\n".join(lines)}

    def close(self):
        if self.client:
            self.client.close()


# get the driver call count from the external environment variables when running on a live agent
# otherwise use hard-coded values below for development
if "VELOCITY_PARAM_call_count" not in os.environ:
    # development area
    callBlock = "1"
    if callBlock == "1":
        os.environ["VELOCITY_PARAM_call_count"] = "1"
        os.environ["VELOCITY_PARAM_call_0"] = "getProperties true"
    elif callBlock == "2":
        os.environ["VELOCITY_PARAM_call_count"] = "1"
        os.environ["VELOCITY_PARAM_call_0"] = "getPorts"

    # hard-coded credentials for dev
    sshUsername = "admin"
    sshPassword = "admin"
    sshServer = "10.36.84.37"
    sshPort = "22"

else:
    sshServer = os.environ["VELOCITY_PARAM_property_ipAddress"]
    sshUsername = os.environ["VELOCITY_PARAM_property_username"]
    sshPassword = os.environ["VELOCITY_PARAM_property_password"]
    sshPort = os.environ.get("VELOCITY_PARAM_property_port", "22")

# open the SSH session to the Ixia chassis
c = IxiaChassis(sshServer, sshUsername, sshPassword, sshPort)

# perform each driver call
for callNumber in range(int(os.environ["VELOCITY_PARAM_call_count"])):
    envVar = os.environ["VELOCITY_PARAM_call_" + str(callNumber)]

    callName = envVar.split()[0]
    callArgs = envVar.split()[1:]

    retVal = (
        eval("c." + callName + "()")
        if len(callArgs) < 1
        else eval("c." + callName + "(callArgs)")
    )
    print(json.dumps(retVal))

# close the ssh session
c.close()
