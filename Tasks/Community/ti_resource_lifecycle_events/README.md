### Project Information:
Project: Velocity Resource Lifecycle Event Scripts (Create, Update and Delete)    
Description: Triggered automation scripts invoked on resource changes introduced in release 9.2    
Category: task    
Class: Community    
  
These scripts are an example implementation for the resource lifecycle event triggers introduced in Velocity 9.2.  Each script will fetch resource information via the Velocity API (but excludes ports in this release) for the resource IDs provided by Velocity in the parameter "resourcesIds".  They then connect to a GitLab instance and project and commit new resources, modifications or deletions.  The user needs to provide the appropriate connection information for a gitlab instance and project.  
  
  
In the event that these scripts are used on an existing inventory, as opposed to a new Velocity instance, the scripts handle the cases where files may or may not exist as expected.  
  
  
Prerequisites:  
  1. Access to an existing or new Velocity instance and an account with admin level access  
  2. Access to either an externally hosted or on-prem instance of GitLab for storing JSON resource data.  NOTE: The scripts have not been tested or developed with GitHub!  
  3. Commit-level access to a GitLab project.  These scripts are configured to use project keys for access, so those will need to be generated.  
    
Handling Sensitive Information:  
  It is best practice to keep passwords and keys out of parameter files, test case files, and other static assets.  Also, sensitive information should not be committed to any repository.  If there is no other option, please keep these values masked.  Secret Parameters will not work in the context of triggered automation, as there is no way for a user to interactively enter the values.  
  
  For executing the scripts in iTest, the user can export the "parameters" page from any of the included .fftc files and fill in the sensitive information there.  Please do not save any of this info in the .fftc files.  
    
  For executin the scripts as triggers in Velocity, the parameter values can be entered in the configuration dialog for the associated triggered task.  

 ----
3 test cases in project
## Test Case File: on_resource_deleted.fftc
### Delete a Velocity Resource from a Gitlab Repository
This script deletes the JSON data associated with a Velocity resource from a gitlab repository.  In the event that the file does not exist, a 400 error is received.
## Test Case File: on_resource_created.fftc
### Create New Velocity Resource in a Gitlab Repository
This script fetches Velocity resource JSON data and creates a file in a gitlab repository.  In the event that the file already exists, an "update" action is performed instead of a "create" action.
## Test Case File: on_resource_modified.fftc
### Update a modified Velocity Resource in a Gitlab Repository
This script fetches Velocity resource JSON data and updates the associated file in a gitlab repository.  In the event that the file doesn't exist, a "create" action is performed instead of an "update" action.