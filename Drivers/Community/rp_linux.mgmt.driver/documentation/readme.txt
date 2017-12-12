Velocity Linux Management Driver

## Requirements
Python on the Agent
    The agent must have Python installed: from the prompt, typing 'python'
    returns the >>> prompt

Python Paramiko module on Agent
    From the >>> prompt, 'import paramiko' runs without failure

SSH login username and password credentials
    Need SSH user credentials to the Linux system

## Customization
Prompt
    The driver uses '$ ' as the current system prompt and this may need to be
    changed by setting 'prompt' in the source file
   
## Installation
Driver Upload
    Zip the contents of this directory (ensuring that manifest.xml is located
    at the root of the file bundle and give the zip file a meaningful name.
    Upload the driver project into Velocity and give it a meaningful name like
    "Linux Management Driver"

Velocity Template
    Duplicate the "Server" template in Velocity and give it a name like
    "Linux Server"
    Ensure the interface type is 'Management'
    Add these two mandatory properties: username and password

Create an Linux server resource
    Create a new resource using the Linux Server template
    Define values of at least these 3 properties on the resource: ipAddress, username,
    and password

Discover the switch's ports
    Click discover on the resource and verify that Hostname, Make, and Model
    are populated as well as the creation of a new port group called 'System'
    that includes the ports on the system 

## Changelog
1.0.0 Initial release

1.0.1 renamed structures from returnJson to returnDictionary to be more accurate

<b>Tags:</b> Driver, Management
