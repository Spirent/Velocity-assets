# HP Device Project
Provides basic commands for management of HP servers.
<b>Tags:</b> Management

1 QuickCall Library in project://ri_hp_5900:
## project://ri_hp_5900/session_profiles/hp_5900_ssh_qc.fftc (project://ri_hp_5900/session_profiles/hp_5900_ssh_qc.fftc)

### addPortToVlan

Argument | Description
------------ | -------------
portName | 
vlanId | 
### removePortFromVlan

Argument | Description
------------ | -------------
portName | 
vlanId | 
### formatPortStatus
Returns JSON formatted string for port status usable by Velocity

Argument | Description
------------ | -------------
portName | 
status | 
### getFirmwareVersion
### getAllPortsStatus
### getBridgeAggregateInterfaces
### addPortToBridgeAggregate

Argument | Description
------------ | -------------
portName | e.g. "FortyGigE1/0/6:1"
bridgeAggNum | an integer
trunk_vlan | 
### removePortFromBridgeAggregate

Argument | Description
------------ | -------------
portName | e.g. "FortyGigE1/0/6:1"
bridgeAggNum | an integer
### enableBridgeAggregate

Argument | Description
------------ | -------------
bagNum | Number of bridge aggregate group to create
### disableBridgeAggregate

Argument | Description
------------ | -------------
bagNum | Number of bridge aggregate group to shutdown
