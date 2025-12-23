Project: Emulated L1 Driver
Description: A NOOP L1 driver useful for testing and validation purposes.
Category: driver
Class: Community
Tags: Driver, Emulated, L1

Model a device called "Emulated L1 Switch" using the "Layer 1 Switch" template, associate it with this driver, and assign it an IP address of 127.0.0.1 (no other properties are required)
Click "Discover" for the driver to auto-populate the port groups and ports
Hidden feature is if you specify an integer value in "Hostname" property, this driver will model that number of blades.
Connect at least two inventory devices to this emulated L1 switch
Create a topology connecting these two devices together with an Ethernet connection
Reserve the topology, and the connection light should go green.
