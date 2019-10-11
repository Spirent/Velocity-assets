### Project Information:
Project: Emulated L2 Driver  
Description: A NOOP L2 driver useful for testing and validation purposes  
Category: driver  
Class: Community  
Tags: Driver, Emulated, L2  
  
Emulated L2 Driver  
Model a device called "Emulated L2 Switch" using the "Layer 2 Switch" switch template, associate it with this driver, and assign it an IP address of 127.0.0.1 (no other properties are required)  
Click "Discover" for the driver to auto-populate the port groups and ports  
Connect at least two inventory devices to this emulated L2 switch  
Create a topology connecting these two devices together with an VLAN connection  
Reserve the topology, and the connection light should go green.  
  

 ----
1 test case in project
## Test Case File: emulated.l2.switch.fftc
### emulated L2
Model a device called "Emulated L2 Switch 1” using the Cisco switch template, associate it with this driver, and assign it an IP address of 127.0.0.1 (no other properties are required)
Click “Discover” for the driver to auto-populate the port groups and ports
Connect at least two inventory devices to this emulated L2 switch
Create a topology connecting these two devices together with a VLAN connection
Reserve the topology, and the connection light should go green.
### getDeviceStatus
### getProperties
### getHostParameter
### getPorts
### getUnwrappedPorts
### addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

### createVlan
### destroyVlan
### addToVlan
### removeFromVlan