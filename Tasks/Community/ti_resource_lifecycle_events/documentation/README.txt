Project: Velocity Resource Lifecycle Events scripts (Create,Update and Delete)  
Description: Scripts for use with Velocity resource triggers provided since release 9.2  
Category: task  
Class: Community  

These scripts are an example implementation for the resource lifecycle event triggers introduced in Velocity 9.2  Each script will fetch resource information via the Velocity API (but excludes ports in this release) for the resource IDs provided by Velocity in the parameter "resourcesIds".  They then connect to a GitLab instance and project and commit new resources, modifications or deletions.  The user needs to provide the appropriate connection information for a gitlab instance and project.

The user should create a parameter file with masked values for credentials and tokens.  Each test case defines and describes the necessary parameters, so saving any of the test case files' parameters page to a parameter file will achieve this goal.  The parameter file should not be uploaded to Velocity, since it potentially contains access keys for the gitlab repository.

In the event that these scripts are used on an existing inventory, as opposed to a new Velocity instance, the scripts handle the cases where files may or may not exist as expected.
