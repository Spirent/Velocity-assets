### Project Information:
Project: Jenkins Velocity Integration  
Description: These scripts will allow Jenking CI/CD developers to reserve a Topology and execute test cases.  
Category: task  
Class: Community  

 ----

## Test Case File: reserveAndExecute.py
### Jenkins Reserve Topology and execute a list of test cases

<table><tr><th>Argument</th><th>Description</th><th>Example</th></tr>
<tr><td>user</td><td>Velocity username to reserve and execute</td><td>admin_user</tr></td>
<tr><td>password</td><td>Velocity password to reserve and execute</td><td>password</tr></td>
<tr><td>baseUrl</td><td>Velocity Url that contains resources and test assets</td><td>https://Velocity.spirent.com</tr></td>
<tr><td>topologyName</td><td>Velocity Topology Name</td><td>Test Topology</tr></td>
<tr><td>automationPathList</td><td>List of Automation assets to execute</td><td>main/ai_spirent/test_cases/traffic_test.fftc</tr></td>
<tr><td>reportdetailLevel</td><td>detail Level for Automation Report</td><td>ALL_ISSUES_ALL_STEPS</tr></td>
<tr><td>testcasetimeout</td><td>Timeout for the test case</td><td>30</tr></td></table>






## Execution Example 
reserveAndExecute.py --automationPathList main/ai_spirent/test_cases/traffic_test.fftc --baseUrl https://Velocity.spirent.com --user admin --password password --topologyName TestTopology --reportdetailLevel ALL_ISSUES_ALL_STEPS --Timeout 30
