### Project Information:
Project: Juniper driver  
Description: Juniper management driver supporting auto-discover of model, version, serial number, and port list; tested with MX480.  
Category: driver  
Class: Community  
  
Juniper Management Driver  
  
The driver implements the management interface and requires the  
following resource properties:  
* ipAddress (optional, but either ipAddress or Hostname must be specified)  
* Hostname (optional, but either ipAddress or Hostname must be specified)  
* username  
* password  
* SSH Port (optional)  
  
The Cisco driver has been tested for model MX480.  

 ----
1 test case in project
## Test Case File: juniper.fftc
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
## Response Map File: show_interfaces.ffrm
## Response Map File: show_interfaces_brief.ffrm
## Response Map File: show_chassis_hardware.ffrm
### show chassis hardware for juniper
1/28/13: NJL inital version.  This is a pretty basic table which is keyed on "item," but there are some things nested under others.  Not sure if this is going to be a problem or not.  For example:

FPC 0            REV 30   750-028467   ABBF8978          MPC 3D 16x 10GE
  CPU            REV 10   711-029089   ABBJ4398          AMPC PMB
  PIC 0                   BUILTIN      BUILTIN           4x 10GE(LAN) SFP+
    Xcvr 0       REV 01   740-031981   17T803100654      SFP+-10G-LR
### show chassis hardware for juniper
1/28/13: NJL inital version.  This is a pretty basic table which is keyed on "item," but there are some things nested under others.  Not sure if this is going to be a problem or not.  For example:

FPC 0            REV 30   750-028467   ABBF8978          MPC 3D 16x 10GE
  CPU            REV 10   711-029089   ABBJ4398          AMPC PMB
  PIC 0                   BUILTIN      BUILTIN           4x 10GE(LAN) SFP+
    Xcvr 0       REV 01   740-031981   17T803100654      SFP+-10G-LR
## Response Map File: show_chassis_firmware.ffrm