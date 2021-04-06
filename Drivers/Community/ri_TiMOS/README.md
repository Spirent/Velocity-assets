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
```
Get available properties of the device. Each property has name and value.

Returns: JSON

Example:
{
  "properties": {
    "physicalClass": "chassis",
    "functionalClass": "Ethernet Switch",
    "description": "Cisco Switch WS-C2960-24TT-L",
    "Make": "Cisco",
    "Model": "WS-C2960-24TT-L",
    "Software Version": "15.0(1)SE3",
    "Software Image": "C2960-LANBASEK9-M",
    "numberPorts": "26",
    "Serial Number": "FOC1050W2ZD"
  },
  "ports": [
    {
      "name": "Fa0/1",
      "status": "offline"
    },
    {
      "name": "Fa0/2",
      "status": "offline"
    },
    {
      "name": "Gi0/1",
      "status": "online"
    }
  ]
}

```

<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><td>true | false

If true, getPorts output will also be included into returned JSON.

</tr></td></table>

### getPorts
```
Get information about device ports and their properties.

This method is also used to determine whether the device is online. If this call ends up with an error, the device is considered offline. Otherwise, the device is considered online.

Returns: JSON

Example:
{
  "ports": [
    {
      "name": "Fa0/1",
      "status": "offline"
    },
    {
      "name": "Fa0/2",
      "status": "offline"
    },
    {
      "name": "Gi0/1",
      "status": "online"
    }
  ]
}
```

4 response maps in project
## Response Map File: show_version.ffrm
## Response Map File: show_chassis.ffrm
## Response Map File: show_port_single.ffrm
## Response Map File: show_port.ffrm