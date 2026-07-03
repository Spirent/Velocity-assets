Project: rp_sonic.l2.switch.driver
Description: SONiC NOS Layer 2 switch driver for Velocity — VLAN lifecycle, baseline/checkpoint teardown, LLDP, port aliases
Category: driver
Class: Community
CreatedBy: rakesh.kumar@keysight.com
Author: rakesh.kumar@keysight.com
Written and debugged by rakesh.kumar@keysight.com
Co-authored-by: Cursor

Port naming:
  Velocity topology ports may use front-panel aliases (e.g. Et1/1) via port_aliases JSON.
  Internal SONiC names are EthernetN. Map aliases in resource properties for AresONE pilot topologies.

Custom procedures (supportCustomArguments):
  setup, teardown, verifyReady, setSpeed, setAdminState, healthcheck, getLldpNeighbors,
  getVlans, createBaseline, listBaselines, runCommand (guarded by allow_run_command)

Dependencies:
  paramiko (Velocity agent host)

Test targets:
  SONiC switch in your lab (set ipAddress in resource properties)
