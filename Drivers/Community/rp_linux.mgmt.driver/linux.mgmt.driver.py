import sys
import os
import paramiko
import time
import logging
import json
import re


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

 
class sshSession:
 
    def __init__(self, address, username, password):
        # connect to linux system via ssh
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
 
    def open(self):
        # invoke a shell on the linux system
        self.shell = self.client.invoke_shell()
 
    def send(self, command):
        # send a command to the linux system
        if(self.shell):
            self.shell.send(command + '\n')
 
    def recv(self, prompt):
        # receive a response from the linux system
        timeout = time.time() + 10
        response = ''
        while not response.endswith(prompt):
            time.sleep(.10)
            if time.time() > timeout:
                break
            else:
                while self.shell.recv_ready():
                    response += self.shell.recv(4096).decode('utf-8').encode('utf-8')
        logger.debug("Full Response: " + response)

        # trim the first line (the command echoed back) and the last line (the prompt)
        trimmedResponse = response.split('\r\n')[1:-1]
        logger.debug("Trimmed RX Response: " + str(trimmedResponse))

        # return the trimmed response
        return trimmedResponse
 
    def getPorts(self):
        # get the ports on the system
        portList = []
        self.send("ls -l /sys/class/net/ |grep --color=never -v /devices/virtual/net |awk '{if(NR>1)print $9}'")
        netList = self.recv(prompt)

        for net in netList:
            # get the link status of each port
            self.send('cat /sys/class/net/'+ net +'/carrier')
            carrier = self.recv(prompt)[0]
            if carrier == '1':
                linkState = 'online'
            else:
                linkState = 'offline'

            # create a port properties dictionary for every port
            portProperties = {"name" : net, "status" : linkState, "container" : "System"}
            logger.debug("Port Properties: " + str(portProperties))

            # add the port port properties to the port list
            portList.append(portProperties)

        # response
        returnDictionary = {'ports' : portList}
        return returnDictionary

    def getProperties(self, args):
        # get the system hostname
        self.send('hostname')
        response1 = self.recv(prompt)

        # get the system make
        self.send('cat /sys/devices/virtual/dmi/id/board_vendor')
        response2 = self.recv(prompt)

        # get the system model
        self.send('cat /sys/devices/virtual/dmi/id/product_name')
        response3 = self.recv(prompt)

        # create resource properties dictionary
        resourceProperties = {"Hostname" : response1[0], "Make" : response2[0], "Model" : response3[0]}

        # response
        returnDictionary = { 'properties' : resourceProperties }

        # include ports in response if argument is true
        if args[0] == 'true':
            portList = self.getPorts()
            returnDictionary['ports'] = portList['ports']

        return returnDictionary

    def close(self):
        if(self.client != None):
            self.client.close()
 
 
# get the driver call count from the external environment variables when running on a live agent
# otherwise use hard-coded values below for development
if 'VELOCITY_PARAM_call_count' not in os.environ:
    # development area
    callBlock = '1'
    if callBlock == '1':
        os.environ["VELOCITY_PARAM_call_count"] = '1'
        os.environ["VELOCITY_PARAM_call_0"] = 'getProperties true'
    elif callBlock == '2':
        os.environ["VELOCITY_PARAM_call_count"] = '1'
        os.environ["VELOCITY_PARAM_call_0"] = 'getPorts'

    # hard-coded credentials and linux host for dev
    sshUsername = 'apt'
    sshPassword = 'spirent'
    sshServer = '10.108.36.168'

else:
    # derive the credentials from the os environment when running on live agent
    sshServer = os.environ["VELOCITY_PARAM_property_ipAddress"]
    sshUsername = os.environ["VELOCITY_PARAM_property_username"]
    sshPassword = os.environ["VELOCITY_PARAM_property_password"]

# the prompt to expect after each command
prompt = '$ '

# open the SSH session to the linux system
c = sshSession(sshServer, sshUsername, sshPassword)
c.open()
c.recv(prompt)

# perform each driver call
for callNumber in range(int(os.environ['VELOCITY_PARAM_call_count'])):
    envVar = os.environ['VELOCITY_PARAM_call_' + str(callNumber)]
    
    # set the call name and arguments
    callName = envVar.split()[0]
    callArgs = envVar.split()[1:]

    # invoke each driver call with arguments and send output to stdout
    retVal = eval('c.'+callName+'()') if len(callArgs) < 1 else eval('c.'+callName+'(callArgs)')
    print(json.dumps(retVal))
    #print(json.dumps(retVal, indent=2))

# close the ssh session
c.close()
