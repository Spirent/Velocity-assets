### Project Information:
Project: Velocity Resource Create,(no) Read, Update, Delete (CRUD) scripts  
Description: Scripts for use with Velocity resource triggers provided since release 9.2
Category: task  
Class: Community  

These scripts fetch resource information via the Velocity API (but excludes ports in this release) for the resource IDs provided by Velocity in the parameter "resourceIds".  They then connect to a GitLab instance and project and commit new resources, modifications or deletions.
The intended use is to create a parameter file with masked values for credentials and tokens.  Each test case defines and describes the necessary parameters.  
  
![Sharing](documentation/resShare.png)  

 ----