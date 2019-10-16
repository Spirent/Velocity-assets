### Project Information:
Project: Big Switch Cloud Fabric L2 Driver    
Description: L2 Velocity driver for Big Switch Cloud Fabric    
Category: driver  
Class: Reference  
  
This is a Velocity Layer 2 driver for the Bigswitch [Big Cloud Fabric(tm)](https://www.bigswitch.com/products/big-cloud-fabric) SDN controller. As the name suggests, this combination of Velocity driver and SDN controller allow you to create a BIG network of leaf switches that can connect devices in Velocity.    
## Driver Download & Installation  
### Download the Drivers  
This L2 infrastructure for Bigswitch Big Cloud Fabric requires TWO driver they are:    
* [Bigswitch Big Cloud Fabric driver](https://developer.spirent.com/zips/velocity/ri_bigswitch_fabric.zip)  
* [Emulated L2 driver](https://developer.spirent.com/zips/velocity/ri_emulated.L2.driver.zip)    
### Install and  Drivers  
The steps to install the above drivers on your Velocity instance are as follows    
1. Download the two drivers mentioned above  
1. Create a new driver named "Big Cloud Fabric L2" and choose the downloaded file "ri_bigswitch_fabric.zip"  
1. Create a new driver named "Emulated L2" and choose the downloaded file "ri_emulated.L2.driver.zip"  
## Creating the Templates  
This L2 infrastructure requrires two inventory templates and one port templates. The templates described below will use default Velocity properties. If you wish to change the property names you will likely need to change the driver.    
### Shared Port Template  
This is a simple port that is shared by default. The steps to create it are:    
1. Create a new template named "Virtual Shared" using "Port" as the parent  
1. Set the "Reservation Type" to "Shared"  
### Leaf Switch Template  
This template describes the leaf/ToR switches that will be connected to Velocity inventory. The steps to build this template are:    
1. Create a new template named "Big Cloud Leaf Switch" using "Layer 2 Switch" as the parent  
1. Set the template to use "Big Cloud Fabric L2" driver  
1. Set the following default values in the template:  
  + ipAddress: IP address or hostname of Bigswitch Fabric controller  
  + username: username for Big Cloud Fabric controller (admin rights)  
  + password: password for Big Cloud Fabric controller  
1. Add a port group named "Virtual", and add one port named "virtual" of template "Virtual Shared"  
1. Add a port group named "Ethernet", but don't add any ports to the template  
### Virtual Spine Template  
This template represents the spine switches in a virtual fashion. This virtual switch creates connections to leaf/tor switches. To create this template do the following:    
1. Create a new template named "Big Cloud Virtual Spine" using "Layer 2 Switch" as the parent  
1. Set the template to use "Emulated L2" driver  
1. Add a port group named "Virtual" (but don't add ports to the template)  
## Add the Devices  
Now that the templates are created, you can add the switches to the inventory.    
### Big Cloud Leaf Switches  
These are the ToR switches. To create these devices do the following for each switch:    
1. Create a leaf switch resource using the "Big Cloud Leaf Switch" template and name it appropiately. Example "Big Cloud Leaf 001"  
1. Add a port for each switch connection that can be connected to a resource. The ports MUST be named using the convention in the Big Cloud Fabric (example: R1L1, R1L2, etc).  Port template should be "Network Port"</li>  
1. Set leaf switch properties as follows:  
  - Name: Same switch name as set in Bigswtich controller.  
  - Hostname: must be same as Name (see above)  
  - ipAddress, username, password: must remain as default for this template (see Leaf Template above)  
  - all others: set as required  
### Big Cloud Virtual Spine  
This infrastructure resource provides a virtual path for DUTs to be connected together that are on different leaf switches. To create this device do the following:    
1. Create a device named "Big Cloud Virtual Spine" using the "Big Cloud Virtual Spine" template  
1. Add a port for each Leaf Switch named "virtual_1 - virtual_<n>" where n = number of leaf swtiches. Port template is "Virtual Shared"  
1. The device properties are not important ... or used in any way  
## Connect Leaf switch to Virtual Spine  
Now that the inventory is complete you can connect the leaf switches to the virtual spine. To make the connections do the following:    
1. Go to the "Big Cloud Virtual Spine" resource page  
1. Click the connect button  
1. For each port named "virtual_<n>" connect it to a corresponding Leaf switches' "virtual" port. There should be one connection per leaf switch.
 ----
1 test case in project
## Test Case File: bigswitch_fabric_driver.fftc
### addToVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>topo_info</td><td>JSON info about the connections to the switch from getTopologyInfo proc</tr></td>
<tr><td>switch_name</td><td>Name of the leaf switch</tr></td></table>

### removeFromVlan
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>topo_info</td><td>JSON info about the connections to the switch from getTopologyInfo proc</tr></td>
<tr><td>switch_name</td><td>Name of the leaf switch</tr></td></table>

### createVlan
### destroyVlan
### getProperties
### getPorts
### getAllResources
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>reservationId</td><td>ID of the reservation</tr></td>
<tr><td>vel_token</td><td>Token to communicate with Velocity</tr></td></table>

### getTopologyInfo
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>reservationId</td><td>ID of the reservation</tr></td></table>

### getHostParameter
### getDeviceStatus
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>deviceHost</td><td>Host name or IP address</tr></td></table>

### cleanVlanList
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>vlan_list</td><td>List of vlans using commas and dashes (example 100,200-203,3002)</tr></td></table>
