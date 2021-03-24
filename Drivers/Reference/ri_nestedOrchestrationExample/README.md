### Project Information:
Project: Velocity Nested Orchestration Examples  
Description: Example nested orchestration driver for orchestrated resources and Velocity selected resources  
Category: driver    
Class: Reference    
    
This is an example Nested Orchestration driver. The driver package contains the manifest file    
and a single fftc file. We encourage you to use the test case's structure (main procedures    
and functional procedures) as an example to implement orchestrated drivers for other devices.    
    
The driver is to be used with a template of interface type "Orchestration" and requires the following Template     
properties:    
  
* property_toDriver and ipAddress (The values of these properties will be passed from Velocity to the driver due to its reference in manifest.xml)   
* property_fromDriver (The value of this property will be passed from the driver to Velocity in initOrchestratedResource)   
  
When using this example for orchestrated resources that contain one or more ports, an L2 switch and driver will need to be implemented  
A resource group called "Group1" must be defined in Velocity already  
  
Optionally, under Inventory/Resources, import the nested.orch.example.1.zip file followed by the nested.orch.example.2.zip file.  
Included in the above is the orchestrated driver, an emulated L2 driver, templates, orchestrated resources, and topologies.  
At the time of this authoring, there were still features being implemented in Velocity to import orchestrated resources, so there are some inconsistencies.  
  

 ----
1 test case in project
## Test Case File: NestedOrchestrationExample.fftc
### Velocity Nested Orchestration Examples
This example driver can be used to develop an understanding of 'orchestrated resources' in Velocity. Upon activation, it instantiates the orchestrated resources in the topology, creates their ports, switch ports and connections. For Velocity selected resources, it initiates the resources selected for the reservation. Upon de-activation, it removes the connections, switch ports, ports, and orchestrated resources. For Velocity selected resources, it terminates the resources selected for the reservation.
### getConfig
### getImage
### getPorts
### getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><tr></tr></table>

### setConfig
### setImage
### initOrchestratedResource
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>id</td><td>The id of the topology resource (Topology context) being initialized</tr></td></table>

### termOrchestratedResource
### initVelocitySelected
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>id</td><td>The id of the topology resource (Topology context) being initialized</tr></td></table>

### termVelocitySelected