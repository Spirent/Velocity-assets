### Project Information:
Project: HP Device Project  
Description: Provides basic commands for management of HP servers.  
Category: driver  
Class: Community  
Tags: Management  

 ----
1 quickcall library in project
## Quickcall Library: hp_5900_ssh_qc.fftc
### addPortToVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portName</td><tr></tr>
<tr><td>vlanId</td><tr></tr></table>

### removePortFromVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portName</td><tr></tr>
<tr><td>vlanId</td><tr></tr></table>

### formatPortStatus
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portName</td><tr></tr>
<tr><td>status</td><tr></tr></table>

### getFirmwareVersion
### getAllPortsStatus
### getBridgeAggregateInterfaces
### addPortToBridgeAggregate
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portName</td><td>e.g. "FortyGigE1/0/6:1"</tr></td>
<tr><td>bridgeAggNum</td><td>an integer</tr></td>
<tr><td>trunk_vlan</td><tr></tr></table>

### removePortFromBridgeAggregate
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portName</td><td>e.g. "FortyGigE1/0/6:1"</tr></td>
<tr><td>bridgeAggNum</td><td>an integer</tr></td></table>

### enableBridgeAggregate
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>bagNum</td><td>Number of bridge aggregate group to create
</tr></td></table>

### disableBridgeAggregate
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>bagNum</td><td>Number of bridge aggregate group to shutdown
</tr></td></table>

1 test case in project
## Test Case File: driver.fftc
### getProperties
### getPorts
### createVlan
### destroyVlan
### addToVlan
### removeFromVlan
4 response maps in project
## Response Map File: display_interface_brief.ffrm
## Response Map File: display_interface_Bridge-Aggregation_brief.ffrm
## Response Map File: display_version.ffrm
## Response Map File: display_device.ffrm