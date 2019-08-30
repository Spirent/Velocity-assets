### Project Information:Project: Python Ping Driver
Description: Python driver for Velocity that checks if a device is online
Category: driver
Class: Community
Tags: Drivers, Management

This driver uses the 'management' interface, where getPorts and getProperties methods are called.
Discover function is supported, but really only returns a 'success' verdict, and no information is 
really discovered. The polling mechanism invokes the getPorts method which pings the ip address 
specified in the 'ipAddress' property. This driver works both on Linux and Windows agents


 ----