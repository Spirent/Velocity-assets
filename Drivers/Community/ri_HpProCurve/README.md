### Project Information:
Project: HP ProCurve
Description: HP ProCurve L2 driver for Velocity VLAN management
Category: driver
Class: Community


 ----
1 test case in project
## Test Case File: hp-procurve-1.1.0.fftc
### getPorts
### getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><tr></tr></table>

### createVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>VLAN ID to manipulate</tr></td></table>

### destroyVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>VLAN ID to manipulate</tr></td></table>

### addToVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>VLAN ID to manipulate</tr></td>
<tr><td>portNumber</td><td>Port number to add/remove to/from VLAN</tr></td>
<tr><td>tagging</td><td>tagged or untagged</tr></td></table>

### removeFromVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>VLAN ID to manipulate</tr></td>
<tr><td>portNumber</td><td>Port number to add/remove to/from VLAN</tr></td>
<tr><td>tagging</td><td>tagged or untagged</tr></td></table>

2 response maps in project
## Response Map File: show_vlan_port.ffrm
## Response Map File: show_interfaces.ffrm