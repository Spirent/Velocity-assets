### Project Information:Project: New User Accounts Driver
Description: New User Accounts Driver
Category: driver
Class: Community

Monitor New User Accounts Driver

<b>Tags:</b> Management

 ----
2 quickcall libraries in project
##Quickcall Library: velocity_rest_qc.fftc
###getUngroupedUsers
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>ignoredUsers</td><td>a space-separated list of usernames to ignore</tr></td></table>

###addUserToGroup
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>userId</td><tr></tr>
<tr><td>groupId</td><td>343282eb-a7f7-4dbe-ab2f-b1d25cf86d79 = shared harness users</tr></td></table>

###enableSystemMessageEmail
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>userId</td><tr></tr></table>

###setEmailAddress
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>userId</td><td>ID of user to modify</tr></td>
<tr><td>username</td><td>email handle.  The LDAP username is sufficient.</tr></td></table>

##Quickcall Library: velocity_db_qc.fftc
###disableCalendarInvitations
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>userId</td><tr></tr></table>

1 test case in project
##Procedure Library: unit_test.fftc
###basicFunctionality
1 test case in project
##Test Case File: driver.fftc
###getPorts
###getProperties
4 response maps in project
##Response Map File: rest_put.ffrm
##Response Map File: user_v1_group_NONE_users.ffrm
##Response Map File: getUngroupedUsers.ffrm
##Response Map File: update_user.ffrm