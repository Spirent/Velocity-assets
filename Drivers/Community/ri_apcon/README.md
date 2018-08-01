2 QuickCall Libraries in project://ri_apcon
2 Procedure Libraries in project://ri_apcon
## Library: project://ri_apcon/session_profiles/process_ref_qc.fftc
## Headline: Process QuickCall library
Description:  
Currently used for ping.  
  
### ping
Determines if device is online. Returns "online", "offline" or "error".

Argument | Description
------------ | -------------
host | IP or Hostname to ping
## Library: project://ri_apcon/session_profiles/ssh_ref_qc.fftc
## Headline: SSH QuickCall Library
Description:  
Just a placeholder for now.  
  
## Library: project://ri_apcon/drivers/apcon-driver.fftc
## Headline: Apcon Driver for Velocity
Description:  
This driver was developed and tested on a multi Blade APCON Layer 1 switch.  It will discover the ports and successfuly connect between end points  
  
### getPorts
Returns information about device ports and their properties.

This method is also used to determine whether the device is online. If this call ends up with an error, the device is considered offline. Otherwise, the device is considered online.

Argument | Description
------------ | -------------
host | IP or hostname of the device
### getProperties
Returns available properties of the device. Each property has name and value.

parameters:
1. arg1 ports - If true, getPorts output will also be included into returned JSON

Argument | Description
------------ | -------------
host | IP or hostname of the device
### connect
Creates a connection between the specified ports: "first port to/bidir second port".
Does nothing if the connection already exists.

Parameters: 
arg1 - first port name
arg2 - second port name
arg3 - connection type: to, bidir

Argument | Description
------------ | -------------
host | IP or hostname of the device<br><br>
### disconnect
Destroys connection between the specified ports.
Does nothing if the connection does not exist.

Parameters: 
arg1 - first port name
arg2 - second port name
arg3 - connection type: to, bidir

Argument | Description
------------ | -------------
host | IP or hostname of the device
### getConnections
Returns a list of all currently connected ports

Parameters: none

Argument | Description
------------ | -------------
host | IP or hostname of the device
## Library: project://ri_apcon/drivers/library.fftc
## Headline: Library Procedures
Description:  
This is the supporting APCON procedure library  
  
### displayInfoMsg

Argument | Description
------------ | -------------
msg | The execution message to display.
### abortExecution

Argument | Description
------------ | -------------
msg | The execution message to display.
### getDeviceHost
First look for property ipAddress. If ipAddress is not defined, look for a value in the Hostname property. If neither is defined, return Error.

Properties:
ipAddress
Hostname
### validateRequiredProperties
Ensure all the  specified properties are available and have values

Argument | Description
------------ | -------------
propNameList | List of property names to validate
### getPortItemList
### getPortItem
Return JSON formatted information.

Argument | Description
------------ | -------------
portName | 
portStatus | 
portContainer | 
