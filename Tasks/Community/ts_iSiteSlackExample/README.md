### Project Information:
Project: Velocity iSite Slack Integration  
Description: iSite application that monitors executions of tests, test suites, and RunLists completed on Velocity by monitoring Kafka and sending notifications to a Slack channel.  
Category: task  
Class: Community  
  
Install these files and the iSite jar file found on Velocity's configure page to /opt/spirent/isite of the host running this task. When running with dryRun = True, it's not necessary to set the Slack webhook and the Bash shell script should be set to print to stdout, not /dev/null.   

 ----