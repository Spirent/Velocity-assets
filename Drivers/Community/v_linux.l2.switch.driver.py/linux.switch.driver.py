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

            # create a port properties dictionary for every port that not excluded
            if net != excludedInterface:
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

    def createVlan(self, args):
        # assign the VLAN Id argument
        vlanId = args[0]

        # create the bridge
        self.send('sudo brctl addbr br-' + vlanId)
        response = self.recv(prompt)

        # enable STP
        self.send('sudo brctl stp br-' + vlanId + ' on')
        response = self.recv(prompt)

        # verify the bridge was created with STP enabled
        self.send("brctl show br-" + vlanId + " | grep --color=never br-" + vlanId + " | awk '{print $1 $3}'")
        assert self.recv(prompt)[0] == 'br-' + vlanId + 'yes'

        # bring up the bridge interface on the system
        self.send('sudo ip link set dev br-' + vlanId + ' up')
        response = self.recv(prompt)

        # verify the bridge interface is up on the system
        self.send('ip link show br-' + vlanId + ' | grep --color=never -o UP')
        assert self.recv(prompt)[0] == 'UP'

    def addToVlan(self, args):
        # assign the arguments
        vlanId = args[0]
        portId = args[1]
        tagSetting = args[2]

        # create a tagged interface if necessary
        if tagSetting == 'tagged':
            # create the tagged interface on the system
            self.send('sudo ip link add link ' + portId + ' name ' + portId + '.' + vlanId + ' type vlan id ' + vlanId)
            response = self.recv(prompt)
            portId = portId+'.'+vlanId
        
            # verify the tagged interface was added to the system
            self.send('ip link show ' + portId)
            assert not re.match('.*does not exist',self.recv(prompt)[0])

        # bring up the interface on the system
        self.send('sudo ip link set dev ' + portId + ' up')
        response = self.recv(prompt)
        
        # verify the interface is up on the system
        self.send('ip link show ' + portId + ' | grep --color=never -o UP')
        assert self.recv(prompt)[0] == 'UP'

        # add the interface to the bridge
        self.send('sudo brctl addif br-' + vlanId + ' ' + portId)
        response = self.recv(prompt)

        # verify the interface was added to the bridge
        self.send('brctl show br-' + vlanId + ' | grep --color=never -o ' + portId + '$')
        assert self.recv(prompt)[0] == portId

    def removeFromVlan(self, args):
        # assign the arguments
        vlanId = args[0]
        portId = args[1]
        tagSetting = args[2]

        # determine if the interface is tagged
        if tagSetting == 'tagged':
            portId = portId+'.'+vlanId

        # remove the interface from the bridge
        self.send('sudo brctl delif br-' + vlanId + ' ' + portId)
        response = self.recv(prompt)

        # verify the interface was removed from the bridge
        self.send('brctl show br-' + vlanId + ' | grep --color=never ' + portId + '$')
        assert len(self.recv(prompt)) == 0

        # remove the interface if it's tagged
        if tagSetting == 'tagged':
            self.send('sudo ip link delete ' + portId)
            response = self.recv(prompt)

            # verify the tagged interface was removed from the system
            self.send('ip link show ' + portId)
            assert re.match('.*does not exist',self.recv(prompt)[0])

    def destroyVlan(self, args):
        # assign the VLAN Id argument
        vlanId = args[0]

        # take down the bridge interface on the system
        self.send('sudo ip link set dev br-' + vlanId + ' down')
        response = self.recv(prompt)

        # verify the bridge interface is down on the system
        self.send('ip link show br-' + vlanId + ' | grep --color=never -o DOWN')
        assert self.recv(prompt)[0] == 'DOWN'

        # delete the bridge
        self.send('sudo brctl delbr br-' + vlanId)
        response = self.recv(prompt)

        # verify the bridge was removed
        self.send("brctl show | grep -o --color=never br-" + vlanId)
        assert len(self.recv(prompt)) == 0

    def close(self):
        if(self.client != None):
            self.client.close()
 
 
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
    elif callBlock == '3':
        os.environ["VELOCITY_PARAM_call_count"] = '3'
        os.environ["VELOCITY_PARAM_call_0"] = 'createVlan 301'
        os.environ["VELOCITY_PARAM_call_1"] = 'addToVlan 301 eth1 untagged'
        os.environ["VELOCITY_PARAM_call_2"] = 'addToVlan 301 eth3 tagged'
    elif callBlock == '4':
        os.environ["VELOCITY_PARAM_call_count"] = '3'
        os.environ["VELOCITY_PARAM_call_0"] = 'removeFromVlan 301 eth1 untagged'
        os.environ["VELOCITY_PARAM_call_1"] = 'removeFromVlan 301 eth3 tagged'
        os.environ["VELOCITY_PARAM_call_2"] = 'destroyVlan 301'

    # hard-coded credentials and linux host for dev
    sshUsername = 'spirent'
    sshPassword = 'spirent'
    sshServer = '10.18.36.168'

else:
    # derive the credentials from the os environment when running on live agent
    sshServer = os.environ["VELOCITY_PARAM_property_ipAddress"]
    sshUsername = os.environ["VELOCITY_PARAM_property_username"]
    sshPassword = os.environ["VELOCITY_PARAM_property_password"]

# the prompt to expect after each command
prompt = '$ '
# the interface to exclude from discovery
# normally this is the management interface of the system 
# which is not a good choice as a bridge interface
excludedInterface = 'eth0'

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

# close the ssh session
c.close()
