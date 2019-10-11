### Project Information:
Project: Emulated L1 Driver  
Description: A NOOP L1 driver useful for testing and validation purposes.  
Category: driver  
Class: Community  
Tags: Driver, Emulated, L1  
  
Model a device called "Emulated L1 Switch" using the MRV template, associate it with this driver, and assign it an IP address of 127.0.0.1 (no other properties are required)  
Click "Discover" for the driver to auto-populate the port groups and ports  
Connect at least two inventory devices to this emulated L1 switch  
Create a topology connecting these two devices together with an Ethernet connection  
Reserve the topology, and the connection light should go green.  
  

 ----
1 test case in project
## Test Case File: emulated.l1.switch.fftc
### emulated L1
Model a device called "Emulated L1 Switch 1” using the MRV template, associate it with this driver, and assign it an IP address of 127.0.0.1 (no other properties are required)
Click “Discover” for the driver to auto-populate the port groups and ports
Connect at least two inventory devices to this emulated L1 switch
Create a topology connecting these two devices together with an Ethernet connection
Reserve the topology, and the connection light should go green.
### getDeviceStatus
### getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><tr></tr></table>

### getHostParameter
### getPorts
### getUnwrappedPorts
### addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

### connect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>firstPort</td><tr></tr>
<tr><td>secondPort</td><tr></tr>
<tr><td>direction</td><tr></tr></table>

### disconnect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>firstPort</td><tr></tr>
<tr><td>secondPort</td><tr></tr>
<tr><td>direction</td><tr></tr></table>
