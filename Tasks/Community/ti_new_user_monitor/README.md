### Project Information:
Monitor New User Accounts Driver  
  
___
<b>Tags:</b> Management  
  
___
2 QuickCall Libraries in project://ti_new_user_monitor
1 Procedure Library in project://ti_new_user_monitor
### Library: project://ti_new_user_monitor/session_profiles/velocity_db_qc.fftc
___
### disableCalendarInvitations

Argument | Description
------------ | -------------
userId | 
### Library: project://ti_new_user_monitor/session_profiles/velocity_rest_qc.fftc
___
### getUngroupedUsers

Argument | Description
------------ | -------------
ignoredUsers | a space-separated list of usernames to ignore
### addUserToGroup

Argument | Description
------------ | -------------
userId | 
groupId | 343282eb-a7f7-4dbe-ab2f-b1d25cf86d79 = shared harness users
### enableSystemMessageEmail

Argument | Description
------------ | -------------
userId | 
### setEmailAddress

Argument | Description
------------ | -------------
userId | ID of user to modify
username | email handle.  The LDAP username is sufficient.
### Library: project://ti_new_user_monitor/test_cases/unit_test.fftc
___
### basicFunctionality
