### Project Information:
Project: Abstract Topology Update  
Description: This task assigns a specific reference session profile to a very non-specific abstract resource.  
Category: task  
Class: Community  
  
AbstractTopologyUpdate utility will update the tbml file of active reservation, if the active reservation does not have abstract resource, script will not modify tbml file. This script changes the tbml of reservation and not the topology, once the reservation is over, changes will not be present.  By default, all the resources in topology will have session associated with them, even this is true for abstract resource, actual resource for abstract resource could be different during reservation, in that scenario there is a need to change the session profile for abstract resource based on which resource resolved. It is mandatory that all the resources in topology (Abstract or Logical) have session profile defined and committed in to the Velocity for the script to run, if resource do not have session profile, script will not update the tbml for reservation.  

 ----
1 quickcall library in project
## Quickcall Library: velocity_qc_lib.fftc
2 test cases in project
## Test Case File: AbstractTopologyWrapper.fftc
## Test Case File: AbstractTopologyUpdate.fftc
### modifyTBML
<table><tr><th>Argument</th><th>Description</th></tr>
<tr><td>origTopology</td><tr></tr>
<tr><td>abstractResources</td><tr></tr></table>

3 response maps in project
## Response Map File: AbstractTopology.ffrm
## Response Map File: eof.ffrm
## Response Map File: puts_line.ffrm