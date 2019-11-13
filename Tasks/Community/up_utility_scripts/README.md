# Useful scripts/utilities to perform time saving tasks

This folder can be used as a collection of tools and utilites that anyone can contribute.


<b>Tags:</b> Examples

This was created to perform scheduled backups, vi cron job or Jenkins, of velocity topologies as an easy way to recover them if someone deletes or modifes them. You can restore the topology using the Velocity UI import operation.

1 \up_utility_scripts\topologies\topologyBackups.py:

**_Note update following variables in script for your environment:_**
baseUrl = 'https://my.velocity.url.com'
apiUser = 'myUsername'
apiPassword = 'myPassword'
baseLogPath = '/my/backup/path/'