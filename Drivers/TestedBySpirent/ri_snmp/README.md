### Project Information:
Project: SNMP driver  
Description: A generic SNMP driver that implements the Management interface  
Category: driver  
Class: TestedBySpirent  
  
A generic SNMP driver that implements the Management interface and requires the following  
resource properties:  
* ipAddress (optional, but either ipAddress or Hostname must be specified)  
* Hostname (optional, but either ipAddress or Hostname must be specified)  
* community  

 ----
1 test case in project
## Test Case File: snmp.fftc
### getDeviceStatus
### getProperties
### getPorts
### addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

### getUnwarppedPorts
### getHostParameter
### findValueByIdx
### findPortByName