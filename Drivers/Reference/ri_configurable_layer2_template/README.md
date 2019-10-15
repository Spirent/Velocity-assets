### Project Information:
Project: Configurable Layer 2 Switch Driver Template  
Description: A template to be used when developing new configurable layer 2 interface drivers  
Category: driver  
Class: Reference  
  
The driver implements the configurable layer 2 interface and requires the  
following resource properties:  
* ipAddress (optional, but either ipAddress or Hostname must be specified)  
* Hostname (optional, but either ipAddress or Hostname must be specified)  
* username  
* password  
* SSH Port (optional)
 ----
1 test case in project
## Test Case File: configurable_layer2.fftc
### isEnoughSpace
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>fileSize</td><td>Size of the desired file in bytes. Will return True if available space is greater than this argument, False otherwise.</tr></td></table>

### setConfig
### setImage
### getConfig
### getImage
### createVlan
### getProperties
### addToVlan
### removeFromVlan
### destroyVlan
### getPorts
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