### Project Information:
Project: ALU TiMOS driver  
Description: Management driver for ALU TiMOS Devices supporting auto-discover of model, version, and port list; tested with TiMOS-B-8.0.R3.  
Category: driver  
Class: Community  
  
ALU TiMOS driver  
  
The driver implements the management interface and requires the  
following resource properties:  
* ipAddress (optional, but either ipAddress or Hostname must be specified)  
* Hostname (optional, but either ipAddress or Hostname must be specified)  
* username  
* password  
* SSH Port (optional)  
  
Tested on TiMOS-B-8.0.R3.  

 ----
1 test case in project
## Test Case File: timos.fftc
### getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><td>true | false

If true, getPorts output will also be included into returned JSON.

</tr></td></table>

### getPorts
4 response maps in project
## Response Map File: show_version.ffrm
## Response Map File: show_chassis.ffrm
## Response Map File: show_port_single.ffrm
## Response Map File: show_port.ffrm