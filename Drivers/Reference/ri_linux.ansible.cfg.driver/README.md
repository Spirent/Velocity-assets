### Project Information:
Project: Velocity Ansible Configurable Driver for Linux  
Description: This is a Velocity reference driver that implements an example Ansible driver in Velocity.  
Category: driver  
Class: Reference  
  
Velocity Ansible Configurable Driver for Linux  
This is a Velocity reference driver that implements an example Ansible driver in Velocity.  
  
Demo Video: https://youtu.be/RJQm1Tu2X0k  
  
Discovery:  
The driver discovers:  
  The ports installed on the Linux host  
  The kernel version of the Linux host  
  The version of curl installed on the Linux host  
    
Polling:  
  When Velocity invokes this driver to poll the Linux host, roughly every 5 minutes,  
  the installed curl version is compared with the curl version set as a property and can message the admin of this change  
    
Configuration via Ansible:  
  When a configuration is specified to be used upon reservation startup, a user can specify which Ansible playbook should be used  
  Optionally, the default configuration can be applied to the Linux host at reservation end - also an Ansible playbook  
    
Requirements:  
  The driver agent must have Ansible installed.  
  For example, on an Ubuntu driver agent:   
    apt-get update ; apt-get -y install software-properties-common  
    apt-add-repository ppa:ansible/ansible -y ; apt-get update  
    apt-get -y install ansible ; apt-get -y install tftp-hpa  
      
  The SSH username must be able to sudo with no password required (NOPASSWD setting)      
    
HOWTO:  
  Import the Linux Ansible template under the velocity.template directory.   
    As admin, go to Inventory, Import, Import from ZIP  
    Point to the ansible.driver.template.zip file and upload  
    Check Velocity messages to verify that one template has been successfully imported  
    
  Change the template's parent  
    Navigate to the newly imported template and "Change Parent" to Server  
    This will add properties like ipAddress and Hostname  
      
  Upload the Ansible driver iTar  
    Export the project to an iTar  
    Upload the iTar as a Driver in Velocity  
      
  Associate the Driver with the Template  
    Navigate to the template and choose the newly uploaded driver   
    Verify that the template is set to "Configurable" interface type  
  
  Create a Linux host resource  
    Create a new resource using the Linux template  
    Assign the ipAddress, SSH username, and SSH password  
    Optionally, assign the Velocity URL, Velocity admin, and Velocity password (to receive detected curl version changes when polling)  
    Click "Discover" and verify that the system's interfaces and Hostname, Curl Version, and Kernel Version properties are detected  
      
  Reserve the resource with an Ansible playbook configuration  
    SSH into the Linux host  
    Create a new reservation on the Linux host with an Ansible playbook     
    Look at the SSH console and verify that a broadcast message appears showing that curl software version has changed   
      
    
     
	  

 ----
1 test case in project
## Test Case File: linux.ansible.driver.1.0.3.fftc
### getProperties
### getPorts
### getPortList
### addPortToJSON
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>portContainer</td><tr></tr>
<tr><td>portStatus</td><tr></tr>
<tr><td>portName</td><tr></tr></table>

### sendChangeMessageToAdmin
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>message</td><tr></tr>
<tr><td>curlVersion</td><tr></tr>
<tr><td>whatChanged</td><tr></tr></table>

### setConfig
3 response maps in project
## Response Map File: ifconfig-a-s.ffrm
## Response Map File: cat_proc_net_dev.ffrm
## Response Map File: ansible-playbook.ffrm