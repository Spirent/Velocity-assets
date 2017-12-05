# Abstract Topoloy Update

This task is useful when abstact resource conditions are so loose that any class of device could be chosen to meet a loose requirement. This task assigns a specific reference session profile to a very non-specific abstract resource.

AbstractTopologyUpdate utility will update the tbml file of active reservation, if the active reservation does not have abstract resource, script will not modify tbml file. This script changes the tbml of reservation and not the topology, once the reservation is over, changes will not be present.  By default, all the resources in topology will have session associated with them, even this is true for abstract resource, actual resource for abstract resource could be different during reservation, in that scenario there is a need to change the session profile for abstract resource based on which resource resolved. It is mandatory that all the resources in topology (Abstract or Logical) have session profile defined and committed in to the Velocity for the script to run, if resource do not have session profile, script will not update the tbml for reservation.

<b>Tags:</b> Examples

1 QuickCall Library in project://a_AbstractTopologyUpdate:
## project://a_AbstractTopologyUpdate/session_profiles/velocity_qc_lib.fftc (project://a_AbstractTopologyUpdate/session_profiles/velocity_qc_lib.fftc)

