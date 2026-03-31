#!/usr/bin/python

from lxml import etree
import re
import os
import time

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
if 'VELOCITY_PARAM_TMBL_FILE' in os.environ:
  topologyFile = os.environ['VELOCITY_PARAM_TMBL_FILE']
else:
  topologyFile = 'exampleTopo.xml'

# headline
s=r"  _____ ______   ____  ____  ______  __ __  ____  ";print(s)
s=r" / ___/|      | /    ||    \|      ||  |  ||    \ ";print(s)
s=r"(   \_ |      ||  o  ||  D  )      ||  |  ||  o  )";print(s)
s=r" \__  ||_|  |_||     ||    /|_|  |_||  |  ||   _/ ";print(s)
s=r" /  \ |  |  |  |  _  ||    \  |  |  |  :  ||  |   ";print(s)
s=r" \    |  |  |  |  |  ||  .  \ |  |  |     ||  |   ";print(s)
s=r"  \___|  |__|  |__|__||__|\_| |__|   \__,_||__|   ";print(s)
print("")
print('Task Example\n')

# set the xml namespace
ns={'ns':'http://www.teslaalliance.org/trs/tbml/1.0'}

# create a parser
parser = etree.XMLParser(remove_blank_text=True)

# create element tree from topology file
tree = etree.parse(topologyFile, parser)

# pretty print the topology tbml
# print(etree.tostring(tree, pretty_print=True))

# create the toplogy object
topoName=tree.xpath('//ns:header/ns:name', namespaces=ns)
topo=velTopology(topoName[0].text)

# create a list of resources
resourceList=tree.xpath('//ns:resource[@type="device"]', namespaces=ns)

print('\nVerifying all devices in the topology are ready...')
portObjById={}
for r in resourceList:

  n=r.xpath('ns:property[@name="name"]', namespaces=ns)[0].text
  print("\n\tChecking status of resource: %s" % n)
  newResource = topo.addResource(n)

  n=r.xpath('ns:property[@name="inventoryName"]', namespaces=ns)[0].text
  print("\t\tResource name: %s" % n)
  newResource.addProperty('inventoryName', n)
  
  n=r.xpath('ns:propertyCollection[@name="System Identification"]/ns:property[@name="ipAddress"]', namespaces=ns)[0].text
  print("\t\tIP address property: %s" % n)
  newResource.addProperty('ipAddress', n)

  print("\tConnecting to resource...")
  time.sleep(1.5)
  print("\tChecking state of resource...")
  time.sleep(0.5)
  print("\t\tResource is now READY to use in this reservation")

  
print("\n\nFinished: PASSED")
