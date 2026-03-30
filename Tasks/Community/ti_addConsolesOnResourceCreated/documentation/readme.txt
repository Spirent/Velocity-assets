Project: Add Console to Orchestrated Resource
Description: Triggered task to add ssh console to ephemeral resource
Category: task
Class: Community

A triggered task that adds an SSH console to an ephemeral resource upon creation. It discovers if ipAddress is defined at the resource level or if the IP address is defined at the port level. Either way, it creates an SSH console on the resource.

![trigger](documentation/screenshot.png)
