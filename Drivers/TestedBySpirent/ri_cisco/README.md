### Project Information:
Project: Cisco driver  
Description: This default Cisco driver works for Cisco Catalyst 3550, 3750, 2960  
Category: driver  
Class: TestedBySpirent  
  
Cisco driver  
  
This default Cisco driver works for Cisco Catalyst 3550. Its structure is very similar to MRV,  
except for L2- and config-specific items. You can use this driver as a stub for implementing  
other L2 drivers.  
  
The driver implements the Configurable Layer 2 Switch interface and requires the  
following resource properties:  
* ipAddress (optional, but either ipAddress or Hostname must be specified)  
* Hostname (optional, but either ipAddress or Hostname must be specified)  
* username  
* password  
  
The Cisco driver has been tested for models 3750 and 2960.  

 ----
1 test case in project
## Test Case File: cisco.fftc
### switchPortToAccessModeIfDynamic
### getIsInTrunkModeByTaggedValue
### parseSessionInfo
### openSession
### getProperties
### addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

### getPorts
### getUnwrappedPorts
### openSessionSimple
### openSessionTryHard
### getDeviceStatus
### createVlan
### batchAddToVlan
### batchRemoveFromVlan
### destroyVlan
### setConfig
### setImage
### reload
### setConfigAndImage
### isEnoughSpace
### getCurrentImage
### backupCurrentImage
### copyFile
### getHostParameter