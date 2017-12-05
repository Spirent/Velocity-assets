# Arista L1 Driver
Provides basic commands for management of Arista L2 switches. 

<b>Tags:</b> L1



1 QuickCall Library in project://d_arista:
## project://d_arista/session_profiles/arista_base_qc.fftc (project://d_arista/session_profiles/arista_base_qc.fftc)

### getInterfaces
### addPortToVlan

Argument | Description
------------ | -------------
vlanId | can be a single number, a range delimited by "-" or a set of numbers delimited by ","
e.g.
    900
    900-905
    900,902,905
portName | 
### removePortFromVlan

Argument | Description
------------ | -------------
vlanId | can be a single number, a range delimited by "-" or a set of numbers delimited by ","
e.g.
    900
    900-905
    900,902,905
portName | 


Created on: Monday December 04 2017 21:25:04 CST
