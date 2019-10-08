### Project Information
This is a Velocity Layer 2 driver for the Bigswitch <a href="https://www.bigswitch.com/products/big-cloud-fabric">Big Cloud Fabric(tm)</a> SDN controller. As the name suggests, this combination of Velocity driver and SDN controller allow you to create a BIG network of leaf switches that can connect devices in Velocity.

Project: Bigswitch Big Cloud Fabric L2 Driver
Category: driver
Class: Community xxx
 ----
# Installation & Configuration
## Installing the Drivers
This L2 infrastructure for Bigswitch Big Cloud Fabric requires TWO driver they are:
<ul>
  <li><a href="https://developer.spirent.com/zips/velocity/ri_bigswitch_fabric.zip"> Bigswitch Big Cloud Fabric driver</a></li>
  <li><a href="https://developer.spirent.com/zips/velocity/ri_emulated.L2.driver.zip"> Emulated L2 driver</a></li>
</ul>
The steps to install the drivers on your Velocity instance are as follows
<ol>
  <li>Download the two drivers mentioned above</li>
  <li>Create a new driver named "Big Cloud Fabric L2" and choose the downloaded file "ri_bigswitch_fabric.zip"</li>
  <li>Create a new driver named "Emulated L2" and choose the downloaded file "ri_emulated.L2.driver.zip"</li>
</ol>
## Creating the Templates
This L2 infrastructure requrires two inventory templates and one port templates. The templates described below will use default Velocity properties. If you wish to change the property names you will likely need to change the driver. 
### Shared Port Temlate
This is a simple port that is shared by default. The steps to create it are:
<ol>
  <li>Create a new template named "Virtual Shared" using "Port" as the parent</li>
  <li>Set the "Reservation Type" to "Shared"</li>
<ol>
### Leaf Switch Template
This template describes the leaf/ToR switches that will be connected to Velocity inventory. The steps to build this template are:
<ol>
  <li>Create a new template named "Big Cloud Leaf Switch" using "Layer 2 Switch" as the parent</li>
  <li>Set the template to use "Big Cloud Fabric L2" driver</li>
  <li>Set the following default values in the template:
     <ul>
       <li>ipAddress: IP address or hostname of Bigswitch Fabric controller</li>
       <li>username: username for Big Cloud Fabric controller (admin rights)</li>
       <li>password: password for Big Cloud Fabric controller</li>
    </ul>  
  </li>
  <li>Add a port group named "Virtual", and add one port named "virtual" of template "Virtual Shared"</li>
  <li>Add a port group named "Ethernet", but don't add any ports to the template</li>
</ol>
### Virtual Spine Template
This template represents the spine switches in a virtual fashion. This virtual switch creates connections to leaf/tor switches. To create this template do the following:
<ol>
  <li>Create a new template named "Big Cloud Virtual Spine" using "Layer 2 Switch" as the parent</li>
  <li>Set the template to use "Emulated L2" driver</li>
  <li>Add a port group named "Virtual" (but don't add ports to the template)</li>
</ol>
## Add the Devices
Now that the templates are created, you can add the switches to the inventory.
### Big Cloud Leaf Switches
These are the ToR switches. To create these devices do the following for each switch:
<ol>
  <li>Create a leaf switch resource using the "Big Cloud Leaf Switch" template and name it appropiately. Example "Big Cloud Leaf 001"</li>
  <li>Add a port for each switch connection that can be connected to a resource. The ports MUST be named using the convention in the Big Cloud Fabric (example: R1L1, R1L2, etc).  Port template should be "Network Port"</li>
  <li>Set leaf switch properties as follows:
     <ul>
        <li>Name: Same switch name as set in Bigswtich controller</li>
        <li>Hostname: must be same as Name (see above).</li>
        <li>ipAddress, username, password: must remain as default for this template (see Leaf Template above)</li>
        <li>all others: set as required</li>                
    </ul>  
</ol>
### Big Cloud Virtual Spine
This infrastructure resource provides a virtual path for DUTs to be connected together that are on different leaf switches. To create this device do the following:
<ol>
  <li>Create a device named "Big Cloud Virtual Spine" using the "Big Cloud Virtual Spine" template</li>
  <li>Add a port for each Leaf Switch named "virtual_1 - virtual_<n>" where n = number of leaf swtiches. Port template is "Virtual Shared"</li>
  <li>The device properties are not important ... or used in any way</li>
</ol>
## Connect Leaf switch to Virtual Spine
Now that the inventory is complete you can connect the leaf switches to the virtual spine. To make the connections do the following:
<ol>
  <li>Go to the "Big Cloud Virtual Spine" resource page</li>
  <li>Click the connect button</li>
  <li>For each port named "virtual_<n>" connect it to a corresponding Leaf switches' "virtual" port. There should be one connection per leaf switch.</li>
</ol>