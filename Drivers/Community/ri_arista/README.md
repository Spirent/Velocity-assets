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
### getPorts
### createVlan
### addToVlan
### removeFromVlan
### destroyVlan
2 response maps in project
## Response Map File: show_interfaces_description.ffrm
## Response Map File: qcGetInterfaces.ffrm