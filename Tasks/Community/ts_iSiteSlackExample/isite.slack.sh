#!/bin/sh
# Don't use duplicate listner/group names. Try using machine name and instance to prevent duplicate listeners
# Change the instance if you have more than one listener 2,3,4...
INSTANCE="1"
#Use the hostname as group assuming hostname is unique
GROUP=$(hostname)
echo "Group Name: ${GROUP}-${INSTANCE}"

# Usage for dryrun. Set dryRun = True in the python script
sudo /usr/bin/java -jar /opt/spirent/isite/velocity-isite.jar -boot vds.example.com:9092 -read Report -group "${GROUP}-${INSTANCE}"  | /usr/bin/jq --unbuffered -c 'select(.type == "REPORT_MESSAGE" and .reportMessage["result"] != null and (.reportMessage["reportId"] | endswith("driver") | not))' | /opt/spirent/isite/isite.py

# Usage for in-service. Set dryRun = False in the python script
# sudo /usr/bin/java -jar /opt/spirent/isite/velocity-isite.jar -boot vds.example.com:9092 -read Report -group "${GROUP}-${INSTANCE}"  | /usr/bin/jq --unbuffered -c 'select(.type == "REPORT_MESSAGE" and .reportMessage["result"] != null and (.reportMessage["reportId"] | endswith("driver") | not))' | /opt/spirent/isite/isite.py > /dev/null 2>&1
