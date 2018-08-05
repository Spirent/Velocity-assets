### Project Information:
Velocity Linux Management Driver  
  
___
## Requirements  
Python on the Agent  
    The agent must have Python installed: from the prompt, typing 'python'  
    returns the >>> prompt  
  
___
Python Paramiko module on Agent  
    From the >>> prompt, 'import paramiko' runs without failure  
  
___
SSH login username and password credentials  
    Need SSH user credentials to the Linux system  
  
___
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
  
___
Velocity Template  
    Duplicate the "Server" template in Velocity and give it a name like  
    "Linux Server"  
    Ensure the interface type is 'Management'  
    Add these two mandatory properties: username and password  
  
___
Create an Linux server resource  
    Create a new resource using the Linux Server template  
    Define values of at least these 3 properties on the resource: ipAddress, username,  
    and password  
  
___
Discover the switch's ports  
    Click discover on the resource and verify that Hostname, Make, and Model  
    are populated as well as the creation of a new port group called 'System'  
    that includes the ports on the system   
  
___
## Changelog  
1.0.0 Initial release  
  
___
1.0.1 renamed structures from returnJson to returnDictionary to be more accurate  
  
___
<b>Tags:</b> Driver, Management  
  
___
