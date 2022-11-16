### Project Information:
Project: MRV driver  
Description: This is the default driver for MRV switches.  
Category: driver  
Class: TestedBySpirent  
  
This is the default driver for MRV switches. The driver package contains the manifest file  
and a single test case. We encourage you to use the test case's structure (main procedures  
and functional procedures) as a stub for implementing drivers for other devices.  
  
The driver implements the Layer 1 Switch interface and requires the following resource  
properties:  
* ipAddress (optional, but either ipAddress or Hostname must be specified)  
* Hostname (optional, but either ipAddress or Hostname must be specified)  
* username  
* password  

 ----
1 test case in project
## Test Case File: mrv-8.6.0.fftc
### convertPortToCSPP
### getConnections
### validatePortState
### batchConnect
### disconnect
### getPorts
### getUnwrappedPorts
### getDeviceStatus
### getProperties
### addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

### getHostParameter