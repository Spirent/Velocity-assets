# F5 Device Project
Provides basic commands for management of F5 equipment.
<b>Tags:</b> Management

2 QuickCall Libraries in project://d_f5:
## project://d_f5/session_profiles/big_ip_base_qc.fftc (project://d_f5/session_profiles/big_ip_base_qc.fftc)

### getActiveVersion
This quickcall returns a JSON value corresponding to the version of the active image on the BigIP.
### getInterfaces
This quickcall returns a JSON list of interface names and statuses
### getRunningState
getRunningState returns the status displayed in the prompt
### setVlan
setVlan adds an interface to the specified vlanID.  vlan name and ip addresses have valid default values

Argument | Description
------------ | -------------
vlanId | VLAN ID to tag this interface to
ifName | interface to add to the VLAN e.g. "1.2"
hostname | hostname of the current BigIP.  This should be retrieved from the topology, as the device may not be configured properly and will likely have "localhost" as the value.
ipAddress | ip address of the interface being added to the VLAN.
cidr | CIDR formatted netmask of the interface we're adding to the VLAN.
vlanName | name of the VLAN we're adding the interface to.
dnsServers | space-separated list of DNS server IP addresses
ntpServer | hostname or IP address of ntp server
fqdn | fqdn for this device.  Well, everything but the hostname.
### clearVlan
clearVlan removes the specified VLAN.

Argument | Description
------------ | -------------
vlanName | Name of VLAN to remove.
### getFirstActivePort
getFirstActivePort returns the name of the first port with the status of "up"
## project://d_f5/session_profiles/big_ip_chassis_qc.fftc (project://d_f5/session_profiles/big_ip_chassis_qc.fftc)

### setVlan
setVlan adds an interface to the specified vlanID.  vlan name and ip addresses have valid default values

Argument | Description
------------ | -------------
vlanId | VLAN ID to tag this interface to
ifName | interface to add to the VLAN e.g. "1.2"
hostname | hostname of the current BigIP.  This should be retrieved from the topology, as the device may not be configured properly and will likely have "localhost" as the value.
ipAddress | ip address of the interface being added to the VLAN.
cidr | CIDR formatted netmask of the interface we're adding to the VLAN.
vlanName | name of the VLAN we're adding the interface to.
trunkName | name of trunk to create
dnsServers | space-separated list of DNS server IP addresses
ntpServer | hostname or IP address of ntp server
fqdn | fqdn for this device.  Well, everything but the hostname.
