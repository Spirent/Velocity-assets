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
### getInterfaces
### getRunningState
### setVlan
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
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanName</td><td>Name of VLAN to remove.</tr></td></table>

### getFirstActivePort
## Quickcall Library: big_ip_chassis_qc.fftc
### setVlan
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
### getPorts
7 response maps in project
## Response Map File: tmsh_save_sys_config.ffrm
## Response Map File: tmsh_show_sys_mcp.ffrm
## Response Map File: qcGetInterfaces.ffrm
## Response Map File: tmsh_show_sys_software.ffrm
## Response Map File: tmsh_show_net_interface.ffrm
## Response Map File: tmsh_show_net_interface_10_2_4.ffrm
## Response Map File: qcGetActiveVersion.ffrm