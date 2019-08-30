### Project Information:Project: Juniper driver
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
##Test Case File: juniper.fftc
###getProperties
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>includePorts</td><td>true | false

If true, getPorts output will also be included into returned JSON.

</tr></td></table>

###getPorts
4 response maps in project
##Response Map File: show_interfaces.ffrm
##Response Map File: show_interfaces_brief.ffrm
##Response Map File: show_chassis_hardware.ffrm
###show chassis hardware for juniper
1/28/13: NJL inital version.  This is a pretty basic table which is keyed on "item," but there are some things nested under others.  Not sure if this is going to be a problem or not.  For example:

FPC 0            REV 30   750-028467   ABBF8978          MPC 3D 16x 10GE
  CPU            REV 10   711-029089   ABBJ4398          AMPC PMB
  PIC 0                   BUILTIN      BUILTIN           4x 10GE(LAN) SFP+
    Xcvr 0       REV 01   740-031981   17T803100654      SFP+-10G-LR
###show chassis hardware for juniper
1/28/13: NJL inital version.  This is a pretty basic table which is keyed on "item," but there are some things nested under others.  Not sure if this is going to be a problem or not.  For example:

FPC 0            REV 30   750-028467   ABBF8978          MPC 3D 16x 10GE
  CPU            REV 10   711-029089   ABBJ4398          AMPC PMB
  PIC 0                   BUILTIN      BUILTIN           4x 10GE(LAN) SFP+
    Xcvr 0       REV 01   740-031981   17T803100654      SFP+-10G-LR
##Response Map File: show_chassis_firmware.ffrm