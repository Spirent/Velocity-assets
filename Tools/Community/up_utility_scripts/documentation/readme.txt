Project: Velocity Admin Scripts/Utilities
Description: Useful scripts/utilities for Velocity admin tasks
Category: library
Class: Community

This folder can be used as a collection of tools and utilities that anyone can contribute to.

#### ..\up_utility_scripts\topologies\topologyBackups.py:

This was created to perform scheduled backups, vi cron job or Jenkins, of velocity topologies as an easy way to recover them if someone deletes or modifes them. You can restore the topology using the Velocity UI import operation.

Note update following variables in script for your environment:
baseUrl = 'https://my.velocity.url.com'
apiUser = 'myUsername'
apiPassword = 'myPassword'
baseLogPath = '/my/backup/path/'