### Project Information:
Calient driver  
  
___
This is the default driver for Calient switches. The driver package contains the manifest file and  
a single test case.  
  
___
The driver implements the Layer 1 Switch interface and requires the following resource  
properties:  
* ipAddress (optional, but if omitted, Hostname must be specified)  
* Hostname (optional, but if omitted, ipAddress must be specified)  
* username - SSH username  
* password - SSH password  
* calientUsername - TL1 session username  
* calientPassword – TL1 session password  
  
___
Note: The Calient driver connects to the switch via an SSH connection using the “username”  
and “password” credentials. Once the SSH connection is established, the TL1 agent> prompt  
will appear, and the driver issues the ACT-USER TL1 command to activate the  
“calientUsername” using its “CalientPassword” password string.  
  
___
This driver requires the following to be configured on the Calient switch:  
* An SSH user account on the Calient switch (the “username” property)  
  
___
By default, an ssh user named “tl1user” exists on the Calient switch as a factory  
default, and this ssh user can be used for the driver's “username” property. This  
account requires no password by default, so the “password” property can remain  
blank.  
* A TL1 user account with provisioning access (the “calientUsername” property)  
  
___
In order to create and remove cross connects, a TL1 account with provisioning  
access must have been provisioned on the Calient switch. By default, a TL1  
user named “admin” exists on the Calient switch as a factory default and can be  
used as the “calientUsername”. The default password for admin is “pxc***”, and  
can be used as the “calientPassword” value.  
  
___
## Readiness check  
Below is a procedure to ensure that the Calient is ready to be managed by the Velocity driver.  
  
___
SSH to the Calient using syntax like: ssh tl1user@10.140.64.30  
* Where tl1user is the ssh username to be used as the “username” property  
* Where the IP address is the Calient's IP address or hostname  
* If necessary, type a password for ssh access (the “password” property)  
* If this step is successful, the agent> prompt should appear in the terminal  
* Activate the user in TL1 with syntax like: act-user::admin:::pxc***  
* Where admin is the TL1 username (the “calientUsername” property”)  
* Where pxc*** is the TL1 password (the “calientPassword” value)  
  
___
If this step is successful, the following response should appear in the terminal:  
  
___
 TL1AGENT 16-12-03 13:45:16  
  
___
M 0 COMPLD  
  
___
 "admin:admin,2"  
  
___
 /* NOTICE This is a private computer system. Unauthorized  
  
___
access or use may lead to prosecution. */  
  
___
;  
  
___
If the SSH connection and activate user operations are successful, the Calient driver configured  
with the appropriate credentials should now auto-discover the Calient ports and allow users to  
create and delete cross-connects.  
  
___
