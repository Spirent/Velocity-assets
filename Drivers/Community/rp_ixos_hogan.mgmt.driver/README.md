### Project Information:
Project: rp_ixos_hogan.mgmt.driver  
Description: AresONE / IxOS Hogan chassis management driver — REST auth, port discovery, LLDP, ownership ops  
Category: driver  
Class: Community  
Tags: Driver, Management, Ixia, AresONE, Hogan, IxOS  
CreatedBy: rakesh.kumar@keysight.com  
Author: rakesh.kumar@keysight.com  
Written and debugged by rakesh.kumar@keysight.com  
Co-authored-by: Cursor  
  
Velocity AresONE / IxOS Hogan Management Driver  
  
## Requirements  
Python on the Agent  
    The agent must have Python installed: from the prompt, typing 'python'  
    returns the >>> prompt  
  
Python requests and paramiko modules on Agent  
    From the >>> prompt, 'import requests' and 'import paramiko' run without failure  
  
SSH and REST credentials  
    Need SSH user credentials to the chassis. REST API uses apiUsername/apiPassword  
    when set; otherwise falls back to username/password.  
  
## Supported Functions  
getProperties [-includePorts true]  
    Returns chassis properties: Hostname, Make (Ixia), Model, SerialNumber,  
    IxOSVersion, ChassisStatus, ManagementIPv4.  
    Pass '-includePorts true' to also return ports in the response.  
  
getPorts  
    Discovers all test ports on the chassis. Port names use AresONE resource-group  
    notation (e.g. "1.1" through "8.2"). Each port includes status (online/offline)  
    and speed/type as container.  
  
getLldpNeighbors  
    Returns LLDP neighbors via SSH show lldp-peer-info data, with REST fallback  
    when useRestApi is true.  
  
takeOwnership <portName>  
    Take ownership of a port by display name (e.g. 1.1). Requires useRestApi=true.  
  
releaseOwnership <portName>  
    Release ownership of a port. Requires useRestApi=true.  
  
rebootPort <portName>  
    Reboot a port. Requires useRestApi=true.  
  
runCommand <command>  
    Executes an arbitrary CLI command on the chassis and returns raw output.  
  
probe  
    Test connectivity. Returns status: ok, auth_failed, or unreachable.  
  
linkCheck [portName]  
    Return link_up/link_state for one port or all ports (Velocity inventory polling).  
  
## Resource Properties  
ipAddress, username, password (required)  
apiUsername, apiPassword (optional REST credentials)  
chassisType (optional: aresone | xgs12 | xgs2)  
useRestApi (optional, default true)  
  
## Installation  
Driver Upload  
    Zip the contents of this directory (ensuring that manifest.xml is located  
    at the root of the file bundle) and give the zip file a meaningful name.  
    Upload the driver project into Velocity.  
  
Velocity Template  
    Under TestEquipment add a new template and give it a name like  
    "AresONE Hogan"  
    Ensure the interface type is 'Management'  
    Add mandatory properties: ipAddress, username, password  
    Add optional properties: apiUsername, apiPassword, chassisType, useRestApi  
  
## Port Naming (AresONE pilot)  
AresONE ports are discovered as 1.1–8.2 (resource-group notation), not raw  
API card.port numbers. Use getLldpNeighbors to validate cabling to adjacent  
switches (e.g. Arista Ethernet17–Ethernet32).  
  
## Changelog  
1.3.0 Reservation lifecycle: setup, verifyReady, teardown, setConfig (rakesh.kumar@keysight.com)  
1.0.0 Initial release  

 ----