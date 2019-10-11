### Project Information:
Project: Netscout Tap Driver  
Description: This is a specialized Netscout driver that enables a circuit to be tapped via the Netscout's internal splitter  
Category: driver  
Class: Community  
  
Video available at: https://youtu.be/Mkj_91ZA524  
  

 ----
1 test case in project
## Test Case File: netscout-tap-driver.fftc
### getConnections
### connect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>port1</td><tr></tr>
<tr><td>port2</td><tr></tr>
<tr><td>direction</td><tr></tr>
<tr><td>softwareType</td><tr></tr></table>

### disconnect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>port1</td><tr></tr>
<tr><td>port2</td><tr></tr>
<tr><td>direction</td><tr></tr>
<tr><td>softwareType</td><tr></tr></table>

### getPorts
### getUnwrappedPorts
### getDeviceStatus
### getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><tr></tr></table>

### addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

### getHostParameter
### isNameTruncated
### getFullPortName
### createVlan
### destroyVlan
3 response maps in project
## Response Map File: connection-info-map.ffrm
## Response Map File: switch-info-map.ffrm
## Response Map File: port-info-map.ffrm