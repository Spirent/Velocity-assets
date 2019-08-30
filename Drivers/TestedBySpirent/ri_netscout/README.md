### Project Information:Project: NetScout driver
Description: This is the default driver for NetScout (OnPath) switches. The driver package contains the
	manifest file and a single test case.
Category: driver
Class: Community

This is the default driver for NetScout (OnPath) switches. The driver package contains the
manifest file and a single test case.

The driver implements the Layer 1 Switch interface and requires the following resource
properties:
* ipAddress (optional, but either ipAddress or Hostname must be specified)
* Hostname (optional, but either ipAddress or Hostname must be specified)
* username - console username
* password - console password
* Protocol (optional, supported values are "SSH" and "Telnet", "SSH" is the default)

 ----
1 test case in project
##Test Case File: netscout.fftc
###getConnections
###connect
###disconnect
###getPorts
###getUnwrappedPorts
###getDeviceStatus
###getProperties
###addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

###getHostParameter
###isNameTruncated
###getFullPortName
3 response maps in project
##Response Map File: connection-info-map.ffrm
##Response Map File: switch-info-map.ffrm
##Response Map File: port-info-map.ffrm