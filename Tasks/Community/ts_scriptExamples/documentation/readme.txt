scriptExamples.zip

This project contains a set of example Python and Bash scripts that may be
helpful to users starting to run external scripts within Velocity. Here is a
brief description of its contents:

timeout.sh - default language and timeout values are over-written. this
demonstrates that the agent aborts execution if not completed within 1 minute
    
execution_env.py - an additional agent requirement product.arch is merged /
added. if there were agent requirements defined in defaultData, they would be
enforced for every script in the project, but in this example, there are no
requirements in that section. there is however, the built-in agent requirement
of language which is always enforced, so this script ultimately has two
requirements: language and product.arch. the script simply shows the current
working directory, the files in that directory, and the environment variables.
parameters added at time of execution will appear as environment variables.

parameters_list.py - this demonstrates how to build a custom command using
specific argument notation, for example --build and --testCaseSpecificParameter.
it also demonstrates how parameters are merged / added with parameters defined
in defaultData. since there is one parameter defined in defaultData, this script
ultimately will prompt the user for two input parameters. this script
demonstrates how a Python script can be executed with custom argument syntax.

robotDemo.rst - this demonstrates the execution of a Robot Framework script. the
commandSequence defined in defaultData is over-written with a custom command
sequence with two items. the first command runs the robot script and the second
command parses the debug file produced in the first step. this demonstrates how
one script execution can actually invoke multiple. this can also be useful to
prepare for a script execution, for example, when an input file needs to be
formulated for subsequent commands in the sequence. this test requires two
additional packages on the agent - robotframework and docutils

legacy/smokeTest1.tcl and legacy/smokeTest2.tcl - this demonstrates bash
executions of legacy scripts like TCL. one fileNameMatch pattern is used to
identify all scripts that are 'runnable' in the legacy library

parseTopologyExample.py - this demonstrates how an input topology can be parsed
in Python. it is intended to be run in conjunction with a topology reservation,
but if not provided, will still run using an example topology file. the script
parses the input topology and allows each topology element to be referenced
using object syntax. the script can be run on a local workstation in interactive
mode by running 'python -i parseTopologyExample.py', and by typing commands like
topo.resources, the user can see the topology contents. this script requires
'lxml' as an additional package

showPythonVersion.py - this simply prints the Python version and takes all its
properties from defaultData

simple.py and simple.sh - these demonstrate the different execution messages
that are classified during execution

velocity_env.py - this demonstrates the ability to perform Velocity REST API
methods on the calling Velocity instance. the script shows the profile of the
user who runs the script using the provided token and URI. if a topology and/or
reservation are assocciated with the execution, that information will also be
shown. this script requires 'requests' as an additional package

## Installation
    Zip the contents of this directory (ensuring that velocity_manifest.json is located
    at the root of the file bundle and give the zip file a meaningful name like ts_scriptExamples.zip
    Upload the zip file into Velocity from the "Automation Assets" tab
    
## Other information:
The script below may be helpful to very quickly upload zipped project bundles to your
Velocity instance:

---------------------------------------
```

#!/bin/bash

fileName=$1
projName=`basename $1 .zip`
velocityUri=https://velocity700a-cal-lab.spirenteng.com
username="spirent"
password="spirent"

zip -f $fileName

curl -X PUT --data-binary "@$1" -H "X-Auth-Token:`curl -s -X GET --user $username:$password $velocityUri/velocity/api/auth/v2/token | python -c \"import sys, json; print json.load(sys.stdin)['token']\"`" $velocityUri/ito/repository/v1/repository/main/$projName -H "Content-Type:application/zip" | python -m json.tool

```
---------------------------------------

Make the necessary changes to velocityUri, username, and password
To use the script, start in some directory like ~/v_scriptExamples where
velocity_manifest.json exists as does your scripts and other folders. 
First, bundle your project with: zip -r scriptExamples.zip *
Second, upload your bundle to Velocity with: ulProj.sh scriptExamples.zip
(where ulProj.sh is the name of this upload script)
The script will freshen your bundle (updating the zip with any changes you have
made to your scripts) and then upload the project to Velocity (replacing any
existing instance of that project)

<b>Tags:</b> Examples
