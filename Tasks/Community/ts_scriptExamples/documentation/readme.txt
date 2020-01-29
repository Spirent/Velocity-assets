Project: Script Examples
Description: This project contains a set of example Python, Bash, Batch, and Powershell scripts that may be helpful to users starting to run external scripts within Velocity
Category: task
Class: Community

This project contains a set of example Python, Bash, Batch, and Powershell
scripts that may be helpful to users starting to run external scripts within
Velocity.

## Installation
    Zip the contents of this directory (ensuring that velocity_manifest.json is located
    at the root of the file bundle and give the zip file a meaningful name like ts_scriptExamples.zip
    Upload the zip file into Velocity from the "Automation Assets" tab

## Contents
    execution_env.py - an additional agent requirement product.arch is merged /
    added. if there were agent requirements defined in defaultData, they would be
    enforced for every script in the project, but in this example, there are no
    requirements in that section. there is however, the built-in agent requirement
    of language which is always enforced, so this script ultimately has two
    requirements: language and product.arch. the script simply shows the current
    working directory, the files in that directory, and the environment variables.
    parameters added at time of execution will appear as environment variables.

    extractedData.py - example script that parses output for measurements and values
    that need to be stored in Elasticsearch for trend analysis and data mining

    parameters_list.py - this demonstrates how to build a custom command using
    specific argument notation, for example --build and --testCaseSpecificParameter.
    it also demonstrates how parameters are merged / added with parameters defined
    in defaultData. since there is one parameter defined in defaultData, this script
    ultimately will prompt the user for two input parameters. this script
    demonstrates how a Python script can be executed with custom argument syntax.

    parameter_types.py - this demonstrates the use of different parameter types
    (text, integer, float, boolean, enum) in a Python script

    parseTopologyExample.py - this demonstrates how an input topology can be parsed
    in Python. it is intended to be run in conjunction with a topology reservation,
    but if not provided, will still run using an example topology file. the script
    parses the input topology and allows each topology element to be referenced
    using object syntax. the script can be run on a local workstation in interactive
    mode by running 'python -i parseTopologyExample.py', and by typing commands like
    topo.resources, the user can see the topology contents. this script requires
    'lxml' as an additional package

    pythonLogging.py - this demonstrates how Velocity displays execution messages
    for different logging levels in Python

    robotDemo.robot - this demonstrates the execution of a Robot Framework script. the
    commandSequence defined in defaultData is over-written with a custom command
    sequence with two items. the first command runs the robot script and the second
    command parses the debug file produced in the first step. this demonstrates how
    one script execution can actually invoke multiple. this can also be useful to
    prepare for a script execution, for example, when an input file needs to be
    formulated for subsequent commands in the sequence. this test requires two
    additional packages on the agent - robotframework and docutils

    showPythonVersion.py - this simply prints the Python version and takes all its
    properties from defaultData

    simple.py, simple.sh, simple.bat, simple.ps1 - these demonstrate the different
    execution messages that are classified during execution

    timeout.sh - default language and timeout values are over-written. this
    demonstrates that the agent aborts execution if not completed within 1 minute

    vbot.example.py - this demonstrates a new feature in 8.1 called vBots. vBots
    are resource-specific automation tasks. When a user opens the topology editor
    of an active reservation and selects a resource, Velocity will display its
    associated vBots. The association is made upon tag intersection, where a script
    tag matches the resource tag. vBots prompt the user for input parameters, but
    it also automatically passes all properties whose name begins with property_
    and will auto-populate the values of those parameters based on the selected
    resource's property value.

    velocity_env.py - this demonstrates the ability to perform Velocity REST API
    methods on the calling Velocity instance. the script shows the profile of the
    user who runs the script using the provided token and URI. if a topology and/or
    reservation are assocciated with the execution, that information will also be
    shown. this script requires 'requests' as an additional package

    velocity_manifest.json - the manifest file describes the contents of a script archive and describes attributes
    of one or more files in the archive. The manifest file can be used for the following purposes:
    • Tell Velocity which parameters requires user input
    • Perform custom execution message parsing
    • Perform verdict parsing based on exit code, output parsing, or both
    • Formulate specific invocations with command line parameter syntax
    • To specify an execution timeout
    • Specify the name, description, and indicate the author of the script for reporting purposes
    • Specify the language for a script that does not have an extension or the correct extension (.py, .bash, .sh)
    • Hide or show the script files in Velocity
    • Perform a script sequence (more than one script action) in an execution
    • Specify additional agent requirements (along with the built-in language requirements)
    This manifest file handles the required properties for each of the scripts in the project

    velocity_manifest_minimal.json - an example manifest file representing the minimum configuration needed to run
    python, shell, batch, or powershell scripts from velocity

    legacy/smokeTest1.tcl and legacy/smokeTest2.tcl - this demonstrates bash
    executions of legacy scripts like TCL. one fileNameMatch pattern is used to
    identify all scripts that are 'runnable' in the legacy library

    pipenv_project/convert.calendar.date.to.julian.py - this demonstrates the use of
    pipenv within a Velocity execution. python-pip and python-virtualenv must be installed on the Velocity agent
    host in advance. The example script is a small example that shows the dependency
    of novas as the required Python package in velagent's virtualenv

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
