Project: Calient Tap Driver
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
