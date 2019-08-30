### Project Information:Project: Ping6 driver
Description: A generic ICMP driver that implements the Management interface.
Category: driver
Class: TestedBySpirent

Ping6 driver

A generic ICMP driver that implements the Management interface. Can be used only for
determine online status of device, port and properties lists always returned empty. The following
resource properties requires:
* ipAddress (optional, but either ipAddress or Hostname must be specified)
* Hostname (optional, but either ipAddress or Hostname must be specified)

 ----
1 test case in project
##Test Case File: ping6.fftc
###getDeviceStatus
###getProperties
###getPorts
###getHostParameter