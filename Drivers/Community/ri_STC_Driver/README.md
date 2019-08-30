### Project Information:Project: Spirent Test Center Management Driver
Description: STC management driver supporting discovery and online check
Category: driver
Class: Community
Tags: Test Equipment, Traffic Generator

This requires access to the STC Lab Server. The driver connects to an STC chassis via the lab server to discover what modules are installed and determine if the chassis is online or offline. The driver is not able to detect link on each port. 

This driver requires a property called STC_Lab_Server to be present in the resource's template. The value of this property is the IP address or hostname of the STC Lab Server.

 ----
1 test case in project
##Test Case File: stc.driver.2.0.3.fftc
This requires access to the STC Lab Server. The driver connects to an STC chassis via the lab server to discover what modules are installed and determine if the chassis is online or offline. The driver is not able to detect link on each port. 

This driver requires a property called STC_Lab_Server to be present in the resource's template. The value of this property is the IP address or hostname of the STC Lab Server.
###getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>rndNum</td><tr></tr></table>

###getPorts
###getPortList
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>slotCount</td><tr></tr>
<tr><td>rndNum</td><tr></tr></table>

###addPortToJSON
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portContainer</td><tr></tr>
<tr><td>portStatus</td><tr></tr>
<tr><td>portName</td><tr></tr></table>

###deleteLabServerConnection
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>rndNum</td><tr></tr></table>

6 response maps in project
##Response Map File: cat_slot_config.ffrm
##Response Map File: serialno.ffrm
##Response Map File: readTestModuleXml.ffrm
##Response Map File: version.ffrm
##Response Map File: getUnwrappedPorts.ffrm
##Response Map File: arp_a.ffrm