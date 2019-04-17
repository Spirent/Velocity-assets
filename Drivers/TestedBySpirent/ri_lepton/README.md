### Project Information:Project: Lepton ColdFusion Driver
Description: This is a supported driver for the 1024 port multirate ColdFusion L1 switch
Category: driver
Class: TestedBySpirent


1) Import the Lepton ColdFusion driver and template (lepton.template.and.driver.zip) in Velocity from Inventory, Resources, Import, Import from Zip
2) Change the Lepton template's parent to "Network Element / Layer 1 Switch"

 ----
1 test case in project
##Test Case File: lepton-1.0.0.fftc
###Lepton Systems (ColdFusion) L1 Switch Driver
Model a device called using the "Lepton ColdFusion Switch" template, associate it with this driver, and assign all required properties.
Click “Discover” for the driver to auto-populate the port groups and ports
Connect at least two inventory devices to this switch.
Create a topology connecting these two devices together with an Ethernet connection.
Reserve the topology, and the connection light should go green.
###getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><tr></tr></table>

###getPorts
###connect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>firstPort</td><tr></tr>
<tr><td>secondPort</td><tr></tr>
<tr><td>direction</td><tr></tr></table>

###disconnect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>firstPort</td><tr></tr>
<tr><td>secondPort</td><tr></tr>
<tr><td>direction</td><tr></tr></table>

###getHostParameter
###getPortModelingId
###getPortLaneStatus
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>laneId</td><td>Lane ID: 1/2/3/4</tr></td>
<tr><td>phyLinkStatus</td><td>PhyLink status: ["UP","UP","UP","UP"]</tr></td></table>

###getMappingDirection
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>direction</td><td>Direction: (bidir) or (to)</tr></td></table>
