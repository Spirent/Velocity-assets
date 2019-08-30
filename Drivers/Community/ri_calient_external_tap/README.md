### Project Information:Project: Calient Tap Driver
Description: This is a specialized Calient driver that enables a circuit to be tapped via an external splitter
Category: driver
Class: Community

Video available at: https://youtu.be/m8DL12m9D8U

1) Import the calient tap template (calient.tap.template.zip) in Velocity from Inventory, Resources, Import, Import from Zip
2) Change the calient tap template's parent to "Network Element / Layer 2 Switch"
3) Define a custom connection type called "Tap" with a custom argument "TxPortToTap" - see screenshot
4) Define a new template called "Tap" with two ports, p0 and p1. Port p0 should have a property "Port Type" of "tap" and port p1 should have a property "Port Type" of "monitor"
5) Create a calient switch in inventory using the supplied template and this calient tap driver
6) Discover the calient switch and ensure that ports are discovered
7) Connect physical resources to the calient switch
8) Use the attached TBML files as examples and start reservations using these sample topologies

Other:
When defining an abstract topology including a tap, the value of "TxPortToTap" should be "AbstractResourceName,AbstractPortName"
When editing a live topology during a reservation and a tap is being added, the value of "TxPortToTap" should be "AbstractResourceName,PhysicalPortName"
For concrete topologies, the value of "TxPortToTap" should be "PhysicalResourceName,PhysicalPortName"

 ----
1 test case in project
##Test Case File: calient-tap-driver.fftc
###convertPortToCSPP
###getConnections
###connect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>port1</td><tr></tr>
<tr><td>port2</td><tr></tr>
<tr><td>direction</td><tr></tr></table>

###disconnect
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>port1</td><tr></tr>
<tr><td>port2</td><tr></tr>
<tr><td>direction</td><tr></tr></table>

###getPorts
###getUnwrappedPorts
###getDeviceStatus
###getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><tr></tr></table>

###addPropToResult
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>json</td><tr></tr>
<tr><td>name</td><tr></tr>
<tr><td>val</td><tr></tr></table>

###getHostParameter
###createVlan
###destroyVlan