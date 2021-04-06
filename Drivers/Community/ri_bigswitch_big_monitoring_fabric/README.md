### Project Information:
Project: Big Switch Big Cloud Monitoring L1 Driver  
Description: Provides a layer 1 driver interface for Big Switch Big Cloud Monitoring.  
Category: driver  
Class: Community  
Tags: L1  

 ----
1 quickcall library in project
## Quickcall Library: big_switch_ssh_base.fftc
### connect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>port1</td><tr></tr>
<tr><td>port2</td><tr></tr>
<tr><td>switch_id</td><tr></tr></table>

### disconnect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>port1</td><tr></tr>
<tr><td>port2</td><tr></tr>
<tr><td>switch_id</td><tr></tr></table>

### getPorts
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>switch_id</td><tr></tr></table>

### getPortState
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>switch_id</td><tr></tr>
<tr><td>interface</td><tr></tr></table>

### getPortsAndStates
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>switch_id</td><tr></tr></table>

### getProperties
### createChainName
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>port1</td><tr></tr>
<tr><td>port2</td><tr></tr>
<tr><td>switch_id</td><tr></tr></table>

1 test case in project
## Procedure Library: driver.fftc
### BigSwitch L1 Switch Driver
How it works.

The BigSwitch has a single controller with multiple switches.  Velocity needs to control the switches individually. To identify the different switches in the ssh session BigSwitch uses MAC addresses of the switches.

The Manifist has the following properties
1. ipAddress : IP of the BigSwitch controller <required>
2. username : login credentials to controller <required>
3. password : login credentials to controller <required>
4. SSH Port : ssh port of BigSwitch controller <optional>
5. Switch Id : MAC address of individual switch managed by BigSwitch controller < required>
### getPorts
```
getPorts returns JSON-formatted port information.  For this driver, we are only concerned with ports in the "up" state.  It ignores any other state.  
```

### connect
### disconnect
### getProperties
### getPortContainer
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>switch_id</td><tr></tr></table>

### addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

2 response maps in project
## Response Map File: show_switch_all_interfaces.ffrm
## Response Map File: show_version.ffrm