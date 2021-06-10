'''

This file was not incuded in the pyvmomi community samples,
and instead was downloaded from
https://github.com/reubenur-rahman/vmware-pyvmomi-examples/blob/master/create_dvs_and_dvport_group.py

'''

import atexit
import sys
import time

from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect

def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """    
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """
    
    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)
    
    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
            print(out)
        else:
            out = '%s completed successfully.' % actionName
            print(out)
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        raise task.info.error
        print(out)
    
    return task.info.result

def get_host(hosts, host_name):
    for host in hosts:
        if host.name == host_name:
            return host

def print_hosts(hosts):
    for host in hosts:
        print("Found host ", host.name)

def get_datacenter(content, dc_name):
    datacenter = get_obj(content, [vim.Datacenter], dc_name)
    return datacenter

def create_dvSwitch(si, content, network_folder, hosts, host_name, dvs_name):
    print("Creating DVS '" + dvs_name + "' on host '" + host_name + "'")
    #pnic_specs = []
    dvs_host_configs = []
    uplink_port_names = []
    dvs_create_spec = vim.DistributedVirtualSwitch.CreateSpec()
    dvs_config_spec = vim.DistributedVirtualSwitch.ConfigSpec()
    dvs_config_spec.name = dvs_name
    #dvs_config_spec.maxPorts = 2000
         
    host = get_host(hosts, host_name)
    dvs_host_config = vim.dvs.HostMember.ConfigSpec()
    dvs_host_config.operation = vim.ConfigSpecOperation.add
    dvs_host_config.host = host
    dvs_host_configs.append(dvs_host_config)
    dvs_config_spec.host = dvs_host_configs

    uplink_port_names.append("dvUplink1")
    dvs_config_spec.uplinkPortPolicy = vim.DistributedVirtualSwitch.NameArrayUplinkPortPolicy()
    dvs_config_spec.uplinkPortPolicy.uplinkPortName = uplink_port_names

    dvs_create_spec.configSpec = dvs_config_spec

    task = network_folder.CreateDVS_Task(dvs_create_spec)
    wait_for_task(task, si)
    print("Successfully created DVS: ", dvs_name)
    return get_obj(content, [vim.DistributedVirtualSwitch], dvs_name)

def add_dvPort_group(si, dv_switch, vlan_id, pg_name):
    print("Creating DV Portgroup '" + pg_name + "' on DVS '" + dv_switch.name + "'")
    dv_pg_spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
    dv_pg_spec.name = pg_name
    dv_pg_spec.numPorts = 1
    dv_pg_spec.type = vim.dvs.DistributedVirtualPortgroup.PortgroupType.earlyBinding

    #VLAN attributes
    start = int(vlan_id)
    end = int(vlan_id)
    dv_pg_spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
    dv_pg_spec.defaultPortConfig.vlan = vim.dvs.VmwareDistributedVirtualSwitch.TrunkVlanSpec()
    dv_pg_spec.defaultPortConfig.vlan.vlanId = [vim.NumericRange(start=start, end=end)]
    dv_pg_spec.defaultPortConfig.vlan.inherited = False

    #Security Policy
    dv_pg_spec.defaultPortConfig.securityPolicy = vim.dvs.VmwareDistributedVirtualSwitch.SecurityPolicy()
    dv_pg_spec.defaultPortConfig.securityPolicy.allowPromiscuous = vim.BoolPolicy(value=True)
    dv_pg_spec.defaultPortConfig.securityPolicy.forgedTransmits = vim.BoolPolicy(value=True)        
    dv_pg_spec.defaultPortConfig.securityPolicy.macChanges = vim.BoolPolicy(value=False)
    dv_pg_spec.defaultPortConfig.securityPolicy.inherited = False

    task = dv_switch.AddDVPortgroup_Task([dv_pg_spec])
    wait_for_task(task, si)
    print("Successfully created DV Portgroup: ", pg_name)

'''
Added as an all-in-one wrapper call to be made from iTest.
'''
def CreateDVSAndPortGroup(si, content, hosts, host_name, datacenter_name, dvs_name, vlan_id, pg_name):
    #Get the Network folder associated with this DC 
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
    network_folder = datacenter.networkFolder
    
    #Create DV Switch
    dv_switch = create_dvSwitch(si, content, network_folder, hosts, host_name, dvs_name)
    
    print("")
    
    #Add port group to this switch
    add_dvPort_group(si, dv_switch, vlan_id, pg_name)

'''
Helper funtion to delete the DVS, which will also delete all the contained Uplinks and Portgroups.
'''
def DeleteDVS(si, content, dvs_name):
    print("Deleting DVS: ", dvs_name)
    dv_switch = get_obj(content, [vim.DistributedVirtualSwitch], dvs_name)
    task = dv_switch.Destroy_Task()
    wait_for_task(task, si)
    print("Successfully deleted DVS: ", dvs_name)

    