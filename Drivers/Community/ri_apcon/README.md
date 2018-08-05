### Project Information:
Project: Apcon  
Description: Velocity driver for IntellaPatch switch, tested with ACI-3030-E32-7 32 Port 1/10/40G Aggregation & Filtering Blade  
Category: drivers  
Class: Community  
  
___
2 QuickCall Libraries in project://ri_apcon
1 Procedure Library in project://ri_apcon
### Library: project://ri_apcon/session_profiles/process_ref_qc.fftc
___
### ping
Determines if device is online. Returns "online", "offline" or "error".

Argument | Description
------------ | -------------
host | IP or Hostname to ping
### Library: project://ri_apcon/session_profiles/ssh_ref_qc.fftc
___
### Library: project://ri_apcon/drivers/library.fftc
___
Headline: Library Procedures
Description:  
THis is the supporting APCON procedure library  
  
### displayInfoMsg

Argument | Description
------------ | -------------
msg | The execution message to display.
### abortExecution

Argument | Description
------------ | -------------
msg | The execution message to display.
### getDeviceHost
### validateRequiredProperties

Argument | Description
------------ | -------------
propNameList | List of property names to validate
### getPortItemList
### getPortItem

Argument | Description
------------ | -------------
portName | 
portStatus | 
portContainer | 
