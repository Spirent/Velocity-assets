Project: Spirent Test Center Management Driver
Description: STC management driver supporting discovery and online check
Category: driver
Class: Community
Tags: Test Equipment, Traffic Generator

This requires access to the STC Lab Server. The driver connects to an STC chassis via the lab server to discover what modules are installed and determine if the chassis is online or offline. The driver is not able to detect link on each port. 

This driver requires a property called STC_Lab_Server to be present in the resource's template. The value of this property is the IP address or hostname of the STC Lab Server.
