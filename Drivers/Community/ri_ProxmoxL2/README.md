### Project Information:
Project: Proxmox L2 Driver    
Description: Proxmox L2 driver to be used with Proxmox instance driver and will manage connections in a Proxmox environment    
Category: driver      
Class: Community      
    
### Abstract:    
    
This is an orchestration driver used deploy dynamically Velocity topologies in an Proxmox server.   
  
This driver is meant to be used in conjunction with the Proxmox driver (ri_Proxmox), and provided templates, so the installation instructions are written assuming that both the switch driver and the instance driver are being used in tandem.    
  
    
### Installation:    
      
Upload the Proxmox instance driver zip to Velocity via "Library / Drivers / Add" and name it something like "Proxmox"    
  
Upload the Proxmox L2 driver zip to Velocity via "Library / Drivers / Add" and name it something like "ProxmoxL2"    
  
Create a template for the proxmox resource and L2, with those properties and types:  
  
*** Resource template**  
  
Inherited from "Orchestrated". It is recommended to create a session that uses ipAddress, username and password properties to login into the created VM.  
  
Group "Proxmox":  
- Proxmox IP address: (Test)  
- Proxmox username: (Text)  
- Proxmox password: (Password)  
  
Group "Template"  
- Template: (Text)  
- Wait IP: (Boolean Yes/No)  
  
Group "VM"  
- Max memory  
- ipAddress  
- CPUs  
- Max disk memory  
- VM name  
- QEMU version  
  
Group "Credentials"  
- username  
- password  
  
** Resource L2**  
  
Inherited from "Layer 2 Switch"  
  
Group "Proxmox":  
- Proxmox IP address: (Test)  
- Proxmox username: (Text)  
- Proxmox password: (Password)  
  
  
Create a Proxmox template, inherited from previous one, of each Proxmox VM template to be managed. It must fulfil those properties  
  
Group "Proxmox":  
- Proxmox IP address: Proxmox cluster IP  
- Proxmox username: Proxmox cluster username  
- Proxmox password: Proxmox cluster password  
  
Group "Template"  
- Template: Template to be deployed (It must exist in the Proxmox cluster)  
- Wait IP: Yes if Velocity should wait for an IP to be assigned, otherwise, select No  
  
Group VM will be filled up by the driver.  
  
Create a Proxmox L2 where properties group Proxmox must be filled up.  
  
Driver support orchestrated resources added ports. It will attach ports to theVM based on those added in the orchestrated resource. Those ports and connections will be added after the VM is deployed and started form the template.  
  
If the VM is connected to a VLAN network, The driver will create a new bridge in the Proxmox server to model this network. One bridge for each network in the topology. The bridge will be destroyed when the reservation ends.  
  
If the Network contains a property called "Proxmox_Network", The driver understands the bridge already exists, so it won't create a new one and will connect the required ports to the bridge with the name of the property value. It is used to connect to external networks or others already created by the admin.  
  

 ----
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
## Test Case File: proxmoxL2-driver-1.0.fftc
### Layer 2 Driver Template
Read the full guide on driver development here:
https://support.spirent.com/SpirentCSC/SC_KnowledgeView?id=DOC10679
### createVlan
### getProperties
### addToVlan
### removeFromVlan
### destroyVlan
### getPorts
```
Get information about device ports and their properties.

This method is also used to determine whether the device is online. If this call ends up with an error, the device is considered offline. Otherwise, the device is considered online.

Returns: JSON

Example:
{
  "ports": [
    {
      "name": "Fa0/1",
      "status": "offline"
    },
    {
      "name": "Fa0/2",
      "status": "offline"
    },
    {
      "name": "Gi0/1",
      "status": "online"
    }
  ]
}
```
