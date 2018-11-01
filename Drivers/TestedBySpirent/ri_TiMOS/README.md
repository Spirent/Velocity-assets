## Library: project://ri_TiMOS/timos.fftc
### getProperties
Get available properties of the device. Each property has name and value.

Returns: JSON

Example:
{
  "properties": {
    "physicalClass": "chassis",
    "functionalClass": "Ethernet Switch",
    "description": "Cisco Switch WS-C2960-24TT-L",
    "Make": "Cisco",
    "Model": "WS-C2960-24TT-L",
    "Software Version": "15.0(1)SE3",
    "Software Image": "C2960-LANBASEK9-M",
    "numberPorts": "26",
    "Serial Number": "FOC1050W2ZD"
  },
  "ports": [
    {
      "name": "Fa0/1",
      "status": "offline"
    },
    {
      "name": "Fa0/2",
      "status": "offline"
    },
    {
      "name": "Gi0/1",
      "status": "online"
    }
  ]
}

Argument | Description
------------ | -------------
includePorts | true | false<br><br>If true, getPorts output will also be included into returned JSON.<br><br>
### getPorts
Get information about device ports and their properties.

This method is also used to determine whether the device is online. If this call ends up with an error, the device is considered offline. Otherwise, the device is considered online.

Returns: JSON

Example:
{
  "ports": [
    {
      "name": "Fa0/1",
      "status": "offline"
    },
    {
      "name": "Fa0/2",
      "status": "offline"
    },
    {
      "name": "Gi0/1",
      "status": "online"
    }
  ]
}
