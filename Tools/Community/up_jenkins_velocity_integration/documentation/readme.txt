Project: Jenkins Velocity Integration  
Description: Allows Jenkins CI/CD developers to reserve a Velocity topology and execute test cases
Category: task  
Class: Community  

 ----

## Test Case File: reserveAndExecute.py
### Jenkins Reserve Topology and execute a list of test cases

<table><tr><th>Argument</th><th>Description</th><th>Example</th></tr>
<tr><td>user</td><td>Velocity username to reserve and execute</td><td>admin_user</tr></td>
<tr><td>password</td><td>Velocity password to reserve and execute</td><td>password</tr></td>
<tr><td>baseUrl</td><td>Velocity Url that contains resources and test assets</td><td>https://Velocity.spirent.com</tr></td>
<tr><td>topologyName</td><td>Velocity Topology Name</td><td>TestTopology</tr></td>
<tr><td>automationPathList</td><td>space sperated automation path assets to execute</td><td>main/ai_spirent/test_cases/test1.fftc main/ai_spirent/test_cases/test2.fftc</tr></td>
<tr><td>reportdetailLevel</td><td>detail Level for Automation Report</td><td>ALL_ISSUES_ALL_STEPS</tr></td>
<tr><td>testcasetimeout</td><td>Timeout for the test case</td><td>30</tr></td></table>


## Usage
This script is used to execute a series of automated test cases in Velocity against a specified topology.  It will return an failed exit code based any input errors or test case failures.  A passed code will result in all test cases executing with a PASSED result.

## Limitations
 - currently does not support spaces in topology name

## reserveAndExecute.py Functionality Overview
 - Validate input arguments  
 - Log on to Velocity with provided user/password - report/exit on failure  
 - Determine the callback url based on system hostname  
 - Determine callback port  
 - Determine TopologyID based on TopologyName from Velocity - report/exit on failure  
 - Reserve Topology - report/exit on failure  
 - Execute test cases against reservation    
 - Return passed/failed test case status  
 - Cancel reservation  





## Execution Example 
reserveAndExecute.py --automationPathList main/ai_spirent/test_cases/test1.fftc main/ai_spirent/test_cases/test2.fftc --baseUrl https://Velocity.spirent.com --user admin --password password --topologyName TestTopology --reportdetailLevel ALL_ISSUES_ALL_STEPS --Timeout 30
