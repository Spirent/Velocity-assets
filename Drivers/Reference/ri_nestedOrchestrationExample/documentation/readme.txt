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

