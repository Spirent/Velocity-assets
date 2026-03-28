### Project Information:
Project: EveNG Instance Driver    
Description: EveNG instance driver that utilizes the orchestrated interface to instantiate new EveNG topologies dynamically, that reflect the Velocity one created    
Category: driver      
Class: Community      
    
    
### Abstract:    
    
This is an orchestration driver used deploy dynamically Velocity topologies in an EveNG server.   
  
This driver is meant to be used in conjunction with the EveNG L2 driver (ri_EvengL2Dyn), and provided templates, so the installation instructions are written assuming that both the switch driver and the instance driver are being used in tandem.    
  
    
### Installation:    
      
Upload the EveNG instance driver zip to Velocity via "Library / Drivers / Add" and name it something like "EveNgDyn"    
  
Upload the EveNG L2 driver zip to Velocity via "Library / Drivers / Add" and name it something like "EveNgL2Dyn"    
  
Create two templates, one for the instances and one for the L2, with those properties and types.  
  
**instances**  
  
Inherited from "Orchestration" template.  
  
Group "Cluster":  
- ClusterIP: (Text)  
- ClusterUsername: (Text)  
- ClusterPassword: (Password)  
  
Group "EVE-NG Temporary"  
- eveng_id: (Text)  
- eveng_ipAddress: (Text)  
- eveng_telnetPort: (Text)  
- eveng_topoLeft: (Text)  
- eveng_topoTop: (Text)  
  
Group "Template Body"  
- template: (Text)  
- type: (Text)  
- image: (Text)  
- icon: (Text)  
- idlepc: (Text)  
- nvram: (Text)  
- ram: (Text)  
- slot1: (Text)  
- slot2: (Text)  
- config: (Text)  
- delay: (Text)  
- left: (Text)  
- top: (Text)  
- postfix:(Text)  
  
** L2 **  
  
Inherited from "Layer 2 Switch" template  
  
Group "Credentials"  
- username: (Text)  
- password: (Password)  
  
  
Create a template inherited from the instance one inherited for each of the nodes available in EveNG. Those fields must be fulfilled:  
  
Group Cluster:  
- ClusterIP: EevNG cluster IP  
- ClusterUsername: Cluster login credentials (username).  
- ClusterPassword: Cluster login credentials (password).  
  
Group Template Body  
- template: EveNG template to use (e.g. c3725). Template won't be created in EveNG, it must exist already.  
- type: Node type (e.g dynamips)  
- image: Firmware image (e.g. c3725-adventerprisek9-mz.124-15.T14.image). Firmware won't be uploaded to EveNG, it must exist already.  
- icon: Icon to be used in EveNG topology (e.g. Router.png). Icon won't be uploaded to EveNG, it must exist already.  
- idlepc: Idle-pc to be configured. Select one of the values offered in EveNG for that architecture/type (e.g. 0x60c08728)  
- nvram: nvram assigned to this node (e.g. 128)  
- ram: ram assigned to this node (e.g. 256)  
- slot1: What is in slot 1 if applicable (e.g. Empty)  
- slot2: What is in slot 2 if applicable (e.g. Empty)  
- config: Config to be loaded (0=no custom config should be loaded, 1=load saved configuration, string=config to load)  
- delay: Delay to start the node in seconds (e.g. 0)  
- left: Left coordinate to place he node in EveNG topology canvas (e.g. 0). nodes can overlap in EveNG visualization with no consequences.  
- top: Top coordinate to place he node in EveNG topology canvas (e.g. 0). nodes can overlap in EveNG visualization with no consequences.  
- postfix: Additional command to be send to QEMU when node is tarted.  
  
Create a template inherited from the L2 one inherited for the associated L2 switches. Those fields must be fulfilled:  
  
- ipAddressP: EevNG cluster IP  
- username: Cluster login credentials (username).  
- password: Cluster login credentials (password).  
  
  
EveNG only allow one session from a single user/pass. That means that the credential used for Velocity must not be used in any other context, as if someone login while velocity is configuring an environment, it will kick our Velocity and so topology instantiation will fail.  
Added to that, Velocity can work in parallel with multiple agents, to deploy several nodes in parallel and speedup the topology deployment. It will cause the same problem as single login session. To solve that, templates restrict agents to those with capabilities "unique: eveng". this must be set in only one agent as a restriction.  
  
EveNG instance driver is linked to EveNG L2 driver.  A resource based on template EVE_NG_L2, using driver ri_evengL2Dyn must be created. Only ipAddress, username and password properties are required, with the right ones to log into EveNG cluster.  
  
# Networking  
  
Taking this topology as example  
  
![Template](documentation/topology.jpeg)   
  
When connecting nodes, regular VLAN links or cloud can be used (Links and blue network in the example).   
  
When connected nodes into external network (purple network), a network with a custom argument named EVE_Network must be used. This argument will contain the port name in EveNG cluster to use to connect to.  
  
![Template](documentation/network.jpeg)  

 ----
2 quickcall libraries in project
## Quickcall Library: velocity_qc.fftc
### getResourceCredentialsByName
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>name</td><tr></tr></table>

### getOrchestratedResourceIdInfo
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>resource_id</td><tr></tr>
<tr><td>reservationId</td><tr></tr></table>

### getTopologyResourcesCoordInfo
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>reservationId</td><tr></tr></table>

### getOrchestratedResourceIdPorts
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>resource_id</td><tr></tr>
<tr><td>reservationId</td><tr></tr></table>

### getReservationConnectionsDetails
## Quickcall Library: eve-ng_qc.fftc
Quickcall library for EVE-NG
### evengLogin
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>username</td><td>eve-ng username</tr></td>
<tr><td>password</td><td>eve-ng password</tr></td></table>

### evengCreateLab
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng session cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (required)</tr></td>
<tr><td>version</td><td>eve-ng lab version (required)</tr></td>
<tr><td>path</td><td>eve-ng lab path</tr></td>
<tr><td>author</td><td>eve-ng lab author</tr></td>
<tr><td>description</td><td>even-ng new lab description</tr></td>
<tr><td>body</td><td>eve-ng new lab body</tr></td></table>

### evengDeleteLab
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng session cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (required)</tr></td></table>

### evengCreateNode
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>node_dict</td><td>eve-ng node template (includes all required properties)</tr></td></table>

### evengStartNode
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>node</td><td>node name to be started</tr></td></table>

### evengStoptNodesAll
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td></table>

### evengGetNode
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>node_id</td><td>eve-ng node id after creation</tr></td></table>

### evengGetNodeID
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>node_name</td><td>eve-ng node id after creation</tr></td></table>

### evengGetNodeInterfaceID
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>node_id</td><td>eve-ng node id after creation</tr></td>
<tr><td>interface_name</td><tr></tr></table>

### evengConnectToNet
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>node_id</td><td>eve-ng node id after creation</tr></td>
<tr><td>interface_id</td><tr></tr>
<tr><td>network_id</td><tr></tr></table>

### evengCreateNodeConnections
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>node_id</td><td>eve-ng node id</tr></td>
<tr><td>network_id</td><td>eve-ng network info
e.g. {"32":"1","21":"2"} where 32 - is port id and 1 - in network id</tr></td>
<tr><td>portName</td><tr></tr></table>

### evengCreateNetwork
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>network</td><tr></tr></table>

### evengGetNetworkID
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>network</td><tr></tr></table>

### evengSetNetworksVisibility
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>cookie</td><td>eve-ng cookie</tr></td>
<tr><td>lab_name</td><td>eve-ng lab name (without .unl)</tr></td>
<tr><td>networks_list</td><td>eve-ng networks list
e.g. [1, 2]</tr></td>
<tr><td>visibility</td><td>eve-ng network id visibility value
e.g. {0, 1}</tr></td></table>

1 test case in project
## Procedure Library: libraryVelocityActions.fftc
### Procedures library for Velocity actions
### getResourceCredentialsByName
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>name</td><tr></tr></table>

### getOrchestratedResourceIdInfo
### getTopologyResourcesCoordInfo
### getOrchestratedResourceIdPorts
### getReservationConnectionsDetails
1 test case in project
## Test Case File: eve-ng-driver-2.0.2.fftc
### EVE-NG Orchestration Driver
### getPorts
### getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><tr></tr></table>

### initOrchestratedResource
### termOrchestratedResource
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>uuid</td><td>If this argument is set, use this rather than from property</tr></td></table>
