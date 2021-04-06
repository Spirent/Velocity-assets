### Project Information:
Project: F5 Device Project  
Description: Provides basic commands for management of F5 equipment.  
Category: driver  
Class: Community  
Tags: Management  

 ----
2 quickcall libraries in project
## Quickcall Library: big_ip_base_qc.fftc
### getActiveVersion
```
This quickcall returns a JSON value corresponding to the version of the active image on the BigIP.
```

### getInterfaces
```
This quickcall returns a JSON list of interface names and statuses
```

### getRunningState
```
getRunningState returns the status displayed in the prompt
```

### setVlan
```
setVlan adds an interface to the specified vlanID.  vlan name and ip addresses have valid default values
```

<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>VLAN ID to tag this interface to</tr></td>
<tr><td>ifName</td><td>interface to add to the VLAN e.g. "1.2"</tr></td>
<tr><td>hostname</td><td>hostname of the current BigIP.  This should be retrieved from the topology, as the device may not be configured properly and will likely have "localhost" as the value.</tr></td>
<tr><td>ipAddress</td><td>ip address of the interface being added to the VLAN.</tr></td>
<tr><td>cidr</td><td>CIDR formatted netmask of the interface we're adding to the VLAN.</tr></td>
<tr><td>vlanName</td><td>name of the VLAN we're adding the interface to.</tr></td>
<tr><td>dnsServers</td><td>space-separated list of DNS server IP addresses</tr></td>
<tr><td>ntpServer</td><td>hostname or IP address of ntp server</tr></td>
<tr><td>fqdn</td><td>fqdn for this device.  Well, everything but the hostname.</tr></td></table>

### clearVlan
```
clearVlan removes the specified VLAN.
```

<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanName</td><td>Name of VLAN to remove.</tr></td></table>

### getFirstActivePort
```
getFirstActivePort returns the name of the first port with the status of "up"
```

## Quickcall Library: big_ip_chassis_qc.fftc
### setVlan
```
setVlan adds an interface to the specified vlanID.  vlan name and ip addresses have valid default values
```

<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>VLAN ID to tag this interface to</tr></td>
<tr><td>ifName</td><td>interface to add to the VLAN e.g. "1.2"</tr></td>
<tr><td>hostname</td><td>hostname of the current BigIP.  This should be retrieved from the topology, as the device may not be configured properly and will likely have "localhost" as the value.</tr></td>
<tr><td>ipAddress</td><td>ip address of the interface being added to the VLAN.</tr></td>
<tr><td>cidr</td><td>CIDR formatted netmask of the interface we're adding to the VLAN.</tr></td>
<tr><td>vlanName</td><td>name of the VLAN we're adding the interface to.</tr></td>
<tr><td>trunkName</td><td>name of trunk to create</tr></td>
<tr><td>dnsServers</td><td>space-separated list of DNS server IP addresses</tr></td>
<tr><td>ntpServer</td><td>hostname or IP address of ntp server</tr></td>
<tr><td>fqdn</td><td>fqdn for this device.  Well, everything but the hostname.</tr></td></table>

2 test cases in project
## Test Case File: unit_test.fftc
## Test Case File: driver.fftc
### getProperties
```
getProperties returns JSON-formatted properties for the device.  It also returns the port data.  The properties gathered will be populated back into velocity for the device.  This is a good way of keeping your inventory up-to-date.
```

### getPorts
```
getPorts returns JSON-formatted port information.  For this driver, we are only concerned with ports in the "up" state.  It ignores any other state.  
```

7 response maps in project
## Response Map File: tmsh_save_sys_config.ffrm
## Response Map File: tmsh_show_sys_mcp.ffrm
## Response Map File: qcGetInterfaces.ffrm
## Response Map File: tmsh_show_sys_software.ffrm
## Response Map File: tmsh_show_net_interface.ffrm
## Response Map File: tmsh_show_net_interface_10_2_4.ffrm
## Response Map File: qcGetActiveVersion.ffrm