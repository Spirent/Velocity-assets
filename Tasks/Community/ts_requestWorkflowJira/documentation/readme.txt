Project: Create Jira Issue
Description: Python reference example triggered automation task for the "On Request Approved" event in Velocity. When a reservation request is accepted, this event fires to parse the reservation request details and opens a task issue in Jira with the user's request.
Category: task
Class: Community

Upload the project zip that includes the python script and manifest file into Velocity. Set the parameter value for jiraUser and jiraPwd to use for the issue to be created in Jira. The script will parse the contents of the reservation request form and populate a new issue of task type in Jira.

![Task](documentation/requestJira.png)
