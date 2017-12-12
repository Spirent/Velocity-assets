Velocity Linux Bridge L2 Switch Driver

## Requirements
Python on the Agent
    The agent must have Python installed: from the prompt, typing 'python'
    returns the >>> prompt

Python Paramiko module on Agent
    From the >>> prompt, 'import paramiko' runs without failure

A Linux host with support for bridging to use as an L2 Switch
    On the linux host being used as an L2 switch, typing 'brctl show' returns
    without failure

SSH login username and password credentials
    Need SSH credentials to the Linux system being used as an L2 switch with
    sudo NOPASSWD enabled
    Once logged into the Linux host, the user can type 'sudo ls' and files are
    listed WITHOUT prompting for a sudo passwd

## Customization
Prompt
    The driver uses '$ ' as the current system prompt and this may need to be
    changed by setting 'prompt' in the source file

Excluded Interface
    This driver's discover capability will find all physical interfaces in the
    system and list them as ports. It is recommended to specify the
    admin/management interface as excluded by setting 'excludedInterface' in
    the source file.
   
## Installation
Driver Upload
    Zip the contents of this directory (ensuring that manifest.xml is located
    at the root of the file bundle and give the zip file a meaningful name.
    Upload the driver project into Velocity and give it a meaningful name like
    "Linux L2 Switch Driver"

Velocity Template
    Duplicate the "Cisco Switch" template in Velocity and give it a name like
    "Linux Switch"
    Change the interface type from 'Configurable Layer 2 Switch' to
    'Layer 2 Switch'
    Set the driver to the driver uploaded in the previous section

Create an L2 switch resource
    Create a new resource using the Linux Switch template
    Define at least these 3 properties on the resource: ipAddress, username,
    and password

Discover the switch's ports
    Click discover on the resource and verify that Hostname, Make, and Model
    are populated as well as the creation of a new port group called 'System'
    that includes the ports to be used for L2 switching 

## Changelog

1.0.1 Initial release

1.0.2 Properly closing the ssh session when done

1.0.3 renamed structures from returnJson to returnDictionary to be more accurate

<b>Tags:</b> Driver, L2
