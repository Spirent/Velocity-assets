### Project Information:
Project: Jenkins Velocity Integration  
Description: These scripts will allow Jenking CI/CD developers to reserve resources and execute test cases.  
Category: task  
Class: Community  

 ----

## Test Case File: reserveAndExecute.py
### Jenkins Reserve Topology and execute a list of test cases

<table><tr><th>Argument</th><th>Description</th><th>Example</th></tr>
<tr><td>user</td><td>Velocity username to reserve and execute</td><td>admin_user</tr></td>
<tr><td>password</td><td>Velocity password to reserve and execute</td><td>password</tr></td>
<tr><td>baseUrl</td><td>Velocity Url that contains resources and test assets</td><td>https://Velocity.spirent.com</tr></td>
<tr><td>topologyId</td><td>Velocity TopologyID to be reserved</td><td>9fa40821-c76a-43dc-b7c7-xxxxxxxxxx</tr></td>
<tr><td>automationPathList</td><td>List of Automation assets to execute</td><td>main/ai_spirent/test_cases/traffic_test.fftc</tr></td>
<tr><td>agentPoolName</td><td>Agent Pool to execute the test case</td><td>cicd</tr></td>
<tr><td>agetCallBackUrl</td><td>Agent that will report results from</td><td>http://agent_cicd.com:</tr></td></table>






## Execution Example 
reserveAndExecute.py --automationPathList main/ai_spirent/test_cases/traffic_test.fftc --baseUrl https://Velocity.spirent.com --user admin --password password --topologyId 9fa40821-c76a-43dc-b7c7-xxxxxxxxxx --agentCallBackUrl http://agent_cicd.com:
