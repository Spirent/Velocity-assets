NetScout driver

This is the default driver for NetScout (OnPath) switches. The driver package contains the
manifest file and a single test case.

The driver implements the Layer 1 Switch interface and requires the following resource
properties:
* ipAddress (optional, but either ipAddress or Hostname must be specified)
* Hostname (optional, but either ipAddress or Hostname must be specified)
* username - console username
* password - console password
* Protocol (optional, supported values are "SSH" and "Telnet", "SSH" is the default)