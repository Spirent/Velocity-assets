# Python Ping Driver


This driver uses the 'management' interface, where getPorts and getProperties methods are called.

Discover function is supported, but really only returns a 'success' verdict, and no information is 

really discovered. The polling mechanism invokes the getPorts method which pings the ip address 

specified in the 'ipAddress' property. This driver works both on Linux and Windows agents



<b>Tags:</b> Drivers, Management



