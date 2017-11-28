import sys
import os
import time
import logging
import json
import re
import subprocess


# create logger and set debugging level
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
#logger.setLevel(logging.DEBUG)
# create console handler and set level
ch = logging.StreamHandler()
# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

 
class pingSession:
 
    def __init__(self):
        pass
 
    def getPorts(self):
        # determine if the system is reachable via ICMP echo request
        if os.name == 'posix':
            ping = subprocess.call(["ping", "-c", "1", ipAddress], stdout=subprocess.PIPE)
        else:
            ping = subprocess.call(["ping", "-n", "1", ipAddress], stdout=subprocess.PIPE)

        if ping == 0:
          returnJson = {"ports":[]}
        else:
            returnJson = {'status': 'unreachable'}

        # JSON response
        return returnJson

    def getProperties(self, args):
        # create resource properties dictionary
        resourceProperties = {}

        # JSON response
        returnJson = { 'properties' : resourceProperties }

        # include ports in response if argument is true
        if args[0] == 'true':
            portList = self.getPorts()
            if portList.has_key('ports'):
                returnJson['ports'] = portList['ports']
            else:
                returnJson = { 'status' : 'unreachable'}


        return returnJson

 
# get the driver call count from the external environment variables when running on a live agent
# otherwise use hard-coded values below for development
if 'VELOCITY_PARAM_call_count' not in os.environ:
    # development area
    callBlock = '2'
    if callBlock == '1':
        os.environ["VELOCITY_PARAM_call_count"] = '1'
        os.environ["VELOCITY_PARAM_call_0"] = 'getProperties true'
    elif callBlock == '2':
        os.environ["VELOCITY_PARAM_call_count"] = '1'
        os.environ["VELOCITY_PARAM_call_0"] = 'getPorts'

    # hard-coded values for dev
    ipAddress = '127.0.0.1'

else:
    # derive the credentials from the os environment when running on live agent
    ipAddress = os.environ["VELOCITY_PARAM_property_ipAddress"]

# open the ping session
c = pingSession()

# perform each driver call
for callNumber in range(int(os.environ['VELOCITY_PARAM_call_count'])):
    envVar = os.environ['VELOCITY_PARAM_call_' + str(callNumber)]

    # set the call name and arguments
    callName = envVar.split()[0]
    callArgs = envVar.split()[1:]

    # invoke each driver call with arguments and send output to stdout
    retVal = eval('c.'+callName+'()') if len(callArgs) < 1 else eval('c.'+callName+'(callArgs)')
    print(json.dumps(retVal, sort_keys=True, indent=4))
