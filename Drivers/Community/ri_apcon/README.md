### Project Information:
Project: Apcon  
Description: Velocity driver for IntellaPatch switch, tested with ACI-3030-E32-7 32 Port 1/10/40G Aggregation & Filtering Blade  
Category: driver  
Class: Community  

 ----
2 quickcall libraries in project
## Quickcall Library: ssh_ref_qc.fftc
## Quickcall Library: process_ref_qc.fftc
### ping
```
Determines if device is online. Returns "online", "offline" or "error".
```

<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>host</td><td>IP or Hostname to ping</tr></td></table>

1 test case in project
## Procedure Library: library.fftc
### Library Procedures
THis is the supporting APCON procedure library
### displayInfoMsg
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>msg</td><td>The execution message to display.</tr></td></table>

### abortExecution
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>msg</td><td>The execution message to display.</tr></td></table>

### getDeviceHost
### validateRequiredProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>propNameList</td><td>List of property names to validate</tr></td></table>

### getPortItemList
### getPortItem
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portName</td><tr></tr>
<tr><td>portStatus</td><tr></tr>
<tr><td>portContainer</td><tr></tr></table>

1 test case in project
## Test Case File: apcon-driver.fftc
### Apcon Driver for Velocity
This driver was developed and tested on a multi Blade APCON Layer 1 switch.  It will discover the ports and successfuly connect between end points
### getPorts
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>host</td><td>IP or hostname of the device</tr></td></table>

### getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>host</td><td>IP or hostname of the device</tr></td></table>

### connect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>host</td><td>IP or hostname of the device</tr></td></table>

### disconnect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>host</td><td>IP or hostname of the device</tr></td></table>

### getConnections
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>host</td><td>IP or hostname of the device</tr></td></table>

3 response maps in project
## Response Map File: show_port_names_A.ffrm
## Response Map File: show_blade_info_all.ffrm
## Response Map File: show_port_info.ffrm