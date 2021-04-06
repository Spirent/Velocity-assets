### Project Information:
Project: Configurable Layer 1 Driver Template  
Description: A template to be used when developing new configurable layer 1 interface drivers  
Category: driver  
Class: Reference  
  
Read the full guide on driver development here:  
https://support.spirent.com/SpirentCSC/SC_KnowledgeView?id=DOC10679  
  
The driver implements the configurable layer 1 interface and requires the  
following resource properties:  
* ipAddress (optional, but either ipAddress or Hostname must be specified)  
* Hostname (optional, but either ipAddress or Hostname must be specified)  
* username  
* password  
* SSH Port (optional)
 ----
1 test case in project
## Test Case File: configurable_layer1.fftc
### Configurable Layer 1 Switch Driver Template
Read the full guide on driver development here:
https://support.spirent.com/SpirentCSC/SC_KnowledgeView?id=DOC10679
### isEnoughSpace
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>fileSize</td><td>Size of the desired file in bytes. Will return True if available space is greater than this argument, False otherwise.</tr></td></table>

### setConfig
### setImage
### getConfig
### getImage
### connect
### disconnect
### getConnections
### getProperties
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

2 response maps in project
## Response Map File: show_interfaces.ffrm
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