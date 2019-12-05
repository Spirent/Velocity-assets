### Project Information:
Project: Jenkins Velocity Integration  
Description: These scripts will allow Jenking CI/CD developers to reserve resources and execute test cases.  
Category: task  
Class: Community  

 ----

## Test Case File: reserveAndExecute.py
### Jenkins Reserve Topology and execute a list of test cases
<table><tr><th>Argument</th><th>Description</th><th>Example</th></tr>
<tr><td>user</td><td>Velocity username to reserve and execute</tr><th>admin_user</th></td></tr>
<tr><td>password</td><td>Velocity password to reserve and execute</tr><th>password</th></td></tr>
<tr><td>baseUrl</td><td>Velocity Url that contains resources and test assets</tr><th>https://Velocity.spirent.com</th></td></tr>
<tr><td>topologyId</td><td>Velocity TopologyID to be reserved</tr><th>9fa40821-c76a-43dc-b7c7-xxxxxxxxxx</th></td></tr>
<tr><td>automationPathList</td><td>List of Automation assets to execute</tr><th>main/ai_spirent/test_cases/traffic_test.fftc</th></td></tr>
<tr><td>agentPoolName</td><td>Agent Pool to execute the test case</tr><th>cicd</th></td></tr>
<tr><td>agetCallBackUrl</td><td>Agent that will report results from</tr><th>http://agent_cicd.com:</th></td></tr><table>






## Execution Example 
reserveAndExecute.py --automationPathList main/ai_spirent/test_cases/traffic_test.fftc --baseUrl https://Velocity.spirent.com --user admin --password password --topologyId 9fa40821-c76a-43dc-b7c7-xxxxxxxxxx --agentCallBackUrl http://agent_cicd.com:
