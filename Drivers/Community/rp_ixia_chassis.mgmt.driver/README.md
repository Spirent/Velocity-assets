### Project Information:
Project: Velocity Ixia Chassis Management Driver  
Description: Python driver for Ixia chassis management via SSH in Velocity  
Category: driver  
Class: Community  
Tags: Driver, Management, Ixia, Chassis  
  
Velocity Ixia Chassis Management Driver  
  
## Requirements  
Python on the Agent  
    The agent must have Python installed: from the prompt, typing 'python'  
    returns the >>> prompt  
  
Python Paramiko module on Agent  
    From the >>> prompt, 'import paramiko' runs without failure  
  
SSH login username and password credentials  
    Need SSH user credentials to the Ixia chassis  
  
## Supported Functions  
getProperties [true|false]  
    Returns chassis properties: Hostname, Make, Model, SerialNumber, ManagementIPv4,  
    ManagementIPv6, IxOSVersion, IxNetworkVersion, LicenseServerVersion, ChassisStatus.  
    Pass 'true' to also return ports in the response.  
  
getPorts  
    Discovers all test ports on the chassis. Each port is identified by  
    port/fanout notation (e.g. "1.1") and set port speed as container.  
  
runCommand <command>  
    Executes an arbitrary CLI command on the chassis and returns raw output.  
  
## Installation  
Driver Upload  
    Zip the contents of this directory (ensuring that manifest.xml is located  
    at the root of the file bundle) and give the zip file a meaningful name.  
    Upload the driver project into Velocity and give it a meaningful name like  
    "Ixia Chassis Management Driver"  
  
Velocity Template  
    Under TestEquipment add a new template and give it a name like  
    "Ixia Chassis"  
    Ensure the interface type is 'Management'  
    Add mandatory properties: ipAddress, username, password  
    Add optional property: port (defaults to 22)  
    Add other optional properties like ManagementIPv6, IxOSVersion, IxNetworkVersion, LicenseServerVersion, ChassisStatus  
  
Create an Ixia chassis resource  
    Create a new resource using the Ixia Chassis template  
    Define values for ipAddress, username, and password  
  
Discover the chassis ports  
    Click Discover on the resource and verify that chassis properties  
    (Hostname, Model, SerialNumber, etc.) are populated and test ports  
    appear grouped by card slot  
  
## Customization  
SSH Prompt  
    The driver uses a 30-second timeout per command. Adjust COMMAND_TIMEOUT  
    in the source file if needed.  
  
## Changelog  
1.0.0 Initial release  

 ----