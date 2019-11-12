#!/usr/bin/python
#####################
## Velocity Topology
# Creates a topology object from a Velocity topology file
# --- Use GetTopo() to retrieve a topology object from the VELOCITY_PARAM_TMBL_FILE environment variable
#       created when any script is run from Velocity
#
#   Topology objects have this structure:
#       topology object
#           +---resource_<resource name>  (resource object)
#               |---props                   (list of all the properties belonging to the resource
#               |---ports                   (list of all the ports belonging to the resource
#               |---prop_<property name>    (string representing the resource property's text)
#               |---port_<port name>        (port object)
#                   +---prop_<port_property_name>    (string representing the port property's text)
# Alex Orr
# Spirent Communications
# 11/12/2019
####################

from lxml import etree
import re, os, sys


def cleanName(string):
    return re.sub('[^a-zA-Z0-9]', '_', string)


class velPort():
    def __init__(self, abstractPortName):
        self.abstractName = abstractPortName
        self.objectName = cleanName(abstractPortName)
        self.props = []

    def addProperty(self, propName, propValue):
        fullName = 'prop_' + cleanName(propName)
        # fullName = cleanName(propName)
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
        # fullName = cleanName(propName)
        self.props.append(fullName)
        setattr(self, fullName, propValue)
        return getattr(self, fullName)

    def addPort(self, abstractPortName):
        fullName = 'port_' + cleanName(abstractPortName)
        # fullName = cleanName(abstractPortName)
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
        self.resources.append(fullName)
        setattr(self, fullName, velResource(abstractResourceName))
        return getattr(self, fullName)


def GetTopo():
    #Get the topology file XML from the parameter supplied by Velocity
    try:
        topologyFile = os.environ['VELOCITY_PARAM_TMBL_FILE']
    except KeyError:
        print('Error: No Velocity Topology Specified')
        sys.exit(1)
    ns = {'ns': 'http://www.teslaalliance.org/trs/tbml/1.0'}
    # create a parser
    parser = etree.XMLParser(remove_blank_text=True)
    # Parse the topology XML
    try:
        tree = etree.parse(topologyFile, parser)
    except:
        print('Error: Unable to open Velocity topology')
        sys.exit(1)

    # create the topology object
    topoName = tree.xpath('//ns:header/ns:name', namespaces=ns)
    topo = velTopology(topoName[0].text)
    # create a list of resources
    resourceList = tree.xpath('//ns:resource[@type="device"]', namespaces=ns)
    #populate the topology object with resources
    for r in resourceList:
        try:
            #Get the name of the current resource and add it to the topology object
            resourceName = r.xpath('ns:property[@name="name"]', namespaces=ns)[0].text
            newResource = topo.addResource(resourceName)
            #Find all the resource's properties and add them to the resource object
            propertyList = r.xpath('ns:property', namespaces=ns)
            for property in propertyList:
                propertyName = property.attrib['name']
                propertyText = property.text
                newResource.addProperty(propertyName,propertyText)
            #Get all the resource's ports and create port objects
            portList = r.xpath('ns:resource[@type="port"]', namespaces=ns)
            for port in portList:
                portName = port.xpath('ns:property[@name="name"]', namespaces=ns)[0].text
                newPort = newResource.addPort(portName)
                #Create property objects for each of the port's properties
                portPropertyList =  port.xpath('ns:property', namespaces=ns)
                for portProperty in portPropertyList:
                    portPropertyName = portProperty.attrib['name']
                    portPropertyText = portProperty.text
                    newPort.addProperty(portPropertyName, portPropertyText)
        except:
            print("Error getting resource")
    # return the topology object
    return topo

