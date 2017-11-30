import sys
import os
import time
import logging
import json
import re
import subprocess

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create file handler which and set level
#fh = logging.FileHandler('/tmp/ping.1.0.1.driver.log')
#fh.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
# add formatter to ch and fh
ch.setFormatter(formatter)
#fh.setFormatter(formatter)
# add ch and fh to logger
logger.addHandler(ch)
#logger.addHandler(fh)

 
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
            returnDictionary = {"ports": []}
        else:
            returnDictionary = {"status": "unreachable"}
            
        return returnDictionary


    def getProperties(self, args):
        # create resource properties dictionary
        resourceProperties = {}

        # create properties dictionary
        returnDictionary = { "properties" : resourceProperties }

        # include ports in response if argument is true
        if args[0] == 'true':
            portList = self.getPorts()
            if portList.has_key('ports'):
                returnDictionary['ports'] = portList['ports']
            else:
                returnDictionary = { "status" : "unreachable"}

        return returnDictionary

# log the environment variables
logger.debug(os.environ)
 
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
    logger.debug(json.dumps(retVal))   
    print(json.dumps(retVal))