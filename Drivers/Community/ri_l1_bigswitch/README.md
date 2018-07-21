1 QuickCall Library in project://ri_l1_bigswitch
1 Procedure Library in project://ri_l1_bigswitch
## Library: project://ri_l1_bigswitch/session_profiles/big_switch_ssh_base.fftc
### connect

Argument | Description
------------ | -------------
port1 | 
port2 | 
switch_id | 
### disconnect

Argument | Description
------------ | -------------
port1 | 
port2 | 
switch_id | 
### getPorts

Argument | Description
------------ | -------------
switch_id | 
### getPortState

Argument | Description
------------ | -------------
switch_id | 
interface | 
### getPortsAndStates

Argument | Description
------------ | -------------
switch_id | 
### getProperties
### createChainName

Argument | Description
------------ | -------------
port1 | 
port2 | 
switch_id | 
## Library: project://ri_l1_bigswitch/test_cases/driver.fftc
## Headline: BigSwitch L1 Switch Driver
Description:  
How it works.  
  
The BigSwitch has a single controller with multiple switches.  Velocity needs to control the switches individually. To identify the different switches in the ssh session BigSwitch uses MAC addresses of the switches.  
  
The Manifist has the following properties  
1. ipAddress : IP of the BigSwitch controller <required>  
2. username : login credentials to controller <required>  
3. password : login credentials to controller <required>  
4. SSH Port : ssh port of BigSwitch controller <optional>  
5. Switch Id : MAC address of individual switch managed by BigSwitch controller < required>  
  
### getPorts
getPorts returns JSON-formatted port information.  For this driver, we are only concerned with ports in the "up" state.  It ignores any other state.  
### connect
### disconnect
### getProperties
### getPortContainer

Argument | Description
------------ | -------------
switch_id | 
### addPropToResult

Argument | Description
------------ | -------------
json | 
name | 
val | 
