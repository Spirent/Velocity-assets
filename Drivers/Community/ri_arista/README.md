### Project Information:
Project: Arista L2 Driver  
Description: Provides basic commands for management of Arista L2 switches.  
Category: driver  
Class: Community  
Tags: L2  

 ----
1 quickcall library in project
## Quickcall Library: arista_base_qc.fftc
### getInterfaces
### addPortToVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>can be a single number, a range delimited by "-" or a set of numbers delimited by ","
e.g.
    900
    900-905
    900,902,905</tr></td>
<tr><td>portName</td><tr></tr></table>

### removePortFromVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlanId</td><td>can be a single number, a range delimited by "-" or a set of numbers delimited by ","
e.g.
    900
    900-905
    900,902,905</tr></td>
<tr><td>portName</td><tr></tr></table>

1 test case in project
## Test Case File: driver.fftc
### getProperties
```
getProperties returns JSON-formatted properties for the device.  It also returns the port data.  The properties gathered will be populated back into velocity for the device.  This is a good way of keeping your inventory up-to-date.
```

### getPorts
```
getPorts returns JSON-formatted port information.  For this driver, we are only concerned with ports in the "up" state.  It ignores any other state.  
```

### createVlan
### addToVlan
### removeFromVlan
### destroyVlan
2 response maps in project
## Response Map File: show_interfaces_description.ffrm
## Response Map File: qcGetInterfaces.ffrm