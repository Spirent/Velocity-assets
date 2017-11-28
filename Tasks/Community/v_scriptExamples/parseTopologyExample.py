#!/usr/bin/python

from lxml import etree
import re
import os

def cleanName(string):
    return re.sub('[^a-zA-Z0-9]', '_', string)
    
class velPort():
    def __init__(self, abstractPortName):
        self.abstractName = abstractPortName
        self.objectName = cleanName(abstractPortName)
        self.props = []

    def addProperty(self, propName, propValue):
        fullName = 'prop_' + cleanName(propName)
        #fullName = cleanName(propName)
        self.props.append(fullName)
        setattr(self, fullName, propValue)
        return getattr(self, fullName)

    def setFarEndPort(self, farEndPortName):
        self.farEndPort = farEndPortName
        
class velResource():
    def __init__(self, abstractResourceName):
        self.abstractName = abstractResourceName
        self.objectName = cleanName(abstractResourceName)
        self.ports = []
        self.props = []

    def __iter__(self):
        return iter(self.ports)

    def addProperty(self, propName, propValue):
        fullName = 'prop_' + cleanName(propName)
        #fullName = cleanName(propName)
        self.props.append(fullName)
        setattr(self, fullName, propValue)
        return getattr(self, fullName)
        
    def addPort(self, abstractPortName):
        fullName = 'port_' + cleanName(abstractPortName)
        #fullName = cleanName(abstractPortName)
        self.ports.append(fullName)
        setattr(self, fullName, velPort(abstractPortName))
        return getattr(self, fullName)

class velTopology():
    def __init__(self, topologyName):
        self.name = topologyName
        self.resources = []

    def __iter__(self):
        return iter(self.resources)

    def addResource(self, abstractResourceName):
        fullName = 'resource_' + cleanName(abstractResourceName)
        #fullName = cleanName(abstractResourceName)
        self.resources.append(fullName)
        setattr(self, fullName, velResource(abstractResourceName))
        return getattr(self, fullName)

# set the topology name
if os.environ.has_key('VELOCITY_PARAM_TMBL_FILE') is True:
  topologyFile = os.environ['VELOCITY_PARAM_TMBL_FILE']
else:
  topologyFile = 'exampleTopo.xml'

# headline
print('\n\nPRETTY PRINTING THE EXAMPLE TOPOLOGY FILE...\n')

# set the xml namespace
ns={'ns':'http://www.teslaalliance.org/trs/tbml/1.0'}

# create a parser
parser = etree.XMLParser(remove_blank_text=True)

# create element tree from topology file
tree = etree.parse(topologyFile, parser)

# pretty print the topology tbml
print(etree.tostring(tree, pretty_print=True))

# create the toplogy object
topoName=tree.xpath('//ns:header/ns:name', namespaces=ns)
topo=velTopology(topoName[0].text)

# create a list of resources
resourceList=tree.xpath('//ns:resource[@type="device"]', namespaces=ns)

print('\n\nPARSING THE TOPOLOGY AND CREATING OBJECT NOTATION...\n')
portObjById={}
i = 1
for r in resourceList:
  print("Found resource %d in topology" % i)

  n=r.xpath('ns:property[@name="name"]', namespaces=ns)[0].text
  print("\tAbstract resource name: %s" % n)
  newResource = topo.addResource(n)

  n=r.xpath('ns:property[@name="inventoryName"]', namespaces=ns)[0].text
  print("\tResolved resource name: %s" % n)
  newResource.addProperty('inventoryName', n)
  
  n=r.xpath('ns:propertyCollection[@name="System Identification"]/ns:property[@name="ipAddress"]', namespaces=ns)[0].text
  print("\tIP address property: %s" % n)
  newResource.addProperty('ipAddress', n)

  portList=r.xpath('ns:resource[@type="port"]', namespaces=ns)
  j = 1
  for p in portList:
    print("\t\tFound port %d under resource %d" % (j, i))

    m=p.xpath('ns:property[@name="name"]', namespaces=ns)[0].text
    print("\t\t\tAbstract port name: %s" % m)
    newPort = newResource.addPort(m)

    newPort.addProperty('id',p.get('id'))
    portObjById[p.get('id')]='topo.resource_'+newResource.objectName+'.port_'+newPort.objectName

    m=p.xpath('ns:property[@name="inventoryName"]', namespaces=ns)[0].text
    print("\t\t\tResolved port name: %s" % m)
    newPort.addProperty('inventoryName', m)

    m=p.xpath('ns:propertyCollection[@name="System Identification"]/ns:property[@name="portNumber"]', namespaces=ns)[0].text
    print("\t\t\tResolved port number: %s" % m)
    newPort.addProperty('portNumber', m)

    j =+ 1
  i += 1

# create a list of links in the topology
links=tree.xpath('//ns:connectivity/ns:link', namespaces=ns)
for i in links:
  endpoints=i.xpath('ns:endpoint', namespaces=ns)
  if len(endpoints) == 2:
    object0=portObjById[endpoints[0].get('id')]
    object1=portObjById[endpoints[1].get('id')]
    eval(object0).setFarEndPort(object1)
    eval(object1).setFarEndPort(object0)
  else:
    print('\n\nERROR: Link was found without two endpoints')

# display examples of object notation based on the sample topology file
if os.environ.has_key('VELOCITY_PARAM_TMBL_FILE') is False:
  print('\n\nSOME EXAMPLES OF USING TOPOLOGY OBJECT NOTATION...\n')
  print('topology name: ' + topo.name)
  # topology name: Any 2 Servers
  print('resources: ' +str(topo.resources))
  # resources: ['resource_Server_2', 'resource_Server_1']
  print('server 1 props: ' + str(topo.resource_Server_1.props))
  # server 1 props: ['prop_inventoryName', 'prop_ipAddress']
  print('server 1 inventoryName: ' + topo.resource_Server_1.prop_inventoryName)
  # server 1 inventoryName: pwrEdge755
  print('server 1 ipAddr: ' + topo.resource_Server_1.prop_ipAddress)
  # server 1 ipAddr: 166.34.10.25
  print('server 1 ports: ' + str(topo.resource_Server_1.ports))
  # server 1 ports: ['port_Port_1']
  print('port 1 props: ' + str(topo.resource_Server_1.port_Port_1.props))
  # port 1 props: ['prop_inventoryName', 'prop_portNumber']
  print('port 1 inventoryName: ' + topo.resource_Server_1.port_Port_1.prop_inventoryName)
  # port 1 inventoryName: eth3
  print('port 1 portNumber: ' + topo.resource_Server_1.port_Port_1.prop_portNumber)
  # port 1 portNumber: 3
  print('port 1 connected to: ' + topo.resource_Server_1.port_Port_1.farEndPort)
  # port 1 connected to: topo.resource_Server_2.port_Port_1
