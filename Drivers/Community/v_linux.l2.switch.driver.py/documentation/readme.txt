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
    Once logged into the Linux host, the user can type 'ssh ls' and files are
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
    Upload the driver project into Velocity and give it a meaningful name like
    "Linux Switch 1.0.0"
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


<b>Tags:</b> Driver, L2