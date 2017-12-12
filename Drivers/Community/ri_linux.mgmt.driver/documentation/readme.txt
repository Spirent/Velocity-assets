Velocity Linux Management Driver

## Requirements
Version 7.0 or later, since it uses the json command introduced in that release

## Customization
Prompt
    The driver uses *# and *$ glob patterns for its system prompt and this may need to be
    changed in the session profile
   
## Installation
Driver Upload
    Export the project as an iTar or use the zip command (ensuring that manifest.xml is located
    at the root of the file bundle) and give the archive file a meaningful name.
    Upload the driver project into Velocity and give it a meaningful name like
    "Linux Management Driver"

Velocity Template
    Duplicate the "Server" template in Velocity and give it a name like "Linux Server"
    Ensure the interface type is 'Management'
    Add these two mandatory properties: SSH_Username and SSH_Password, and this optional property: Kernel_Release

Create an Linux server resource
    Create a new resource using the Linux Server template
    Define values of at least these 3 properties on the resource: ipAddress, SSH_Username, and SSH_Password    

Discover the switch's ports
    Click discover on the resource and verify that Hostname and Kernel_Release
    are populated as well as the creation of a new port group called 'ports'
    that includes the ports on the system 

## Changelog
1.0.0 Initial release


<b>Tags:</b> Driver, Management
