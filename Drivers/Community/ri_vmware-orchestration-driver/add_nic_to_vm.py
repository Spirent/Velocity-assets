"""
Written by nickcooper-zhangtonghao
Github: https://github.com/nickcooper-zhangtonghao
Email: nickcooper-zhangtonghao@opencloud.tech

Note: Example code For testing purposes only

This code has been released under the terms of the Apache-2.0 license
http://opensource.org/licenses/Apache-2.0
"""
from pickle import TRUE
from tools import tasks

def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def add_nic(si, uuid):
    """
    :param si: Service Instance
    :param uuid: Virtual Machine UUID    
    """
    
    from pyVmomi import vim
    
    vm = si.content.searchIndex.FindByUuid(None,uuid,True,False)

    if vm is None:
        raise SystemExit(
            "Unable to locate VirtualMachine for uuid {0}"
            .format(uuid)
            )


    spec = vim.vm.ConfigSpec()
    nic_changes = []

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

    """
    
    Ensure we use the correct Network Adpater Type.
    
    #nic_spec.device = vim.vm.device.VirtualE1000()      # The E1000 virtual Ethernet adapter
    #nic_spec.device = vim.vm.device.VirtualVmxnet()     # The Vmxnet virtual Ethernet adapter (generic)
    #nic_spec.device = vim.vm.device.VirtualVmxnet2()    # The Vmxnet2 virtual Ethernet adapter
    #nic_spec.device = vim.vm.device.VirtualVmxnet3()    # The Vmxnet3 virtual Ethernet adapter
    """
    nic_spec.device = vim.vm.device.VirtualVmxnet3()
    

    nic_spec.device.deviceInfo = vim.Description()
    nic_spec.device.deviceInfo.summary = ''

    content = si.RetrieveContent()

    nic_spec.device.backing = \
    vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nic_spec.device.backing.useAutoDetect = False

    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.allowGuestControl = True
    nic_spec.device.connectable.connected = True
    nic_spec.device.connectable.status = 'untried'
    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = 'assigned'

    nic_changes.append(nic_spec)
    spec.deviceChange = nic_changes
    e = vm.ReconfigVM_Task(spec=spec)
    tasks.wait_for_tasks(si, [e])
    
    # show the last nic added
    content = si.RetrieveContent()
    for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                nicspec = vim.vm.device.VirtualDeviceSpec()
                #nicspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit                    
                nicspec.device = device    

                
    print(nicspec)            
                
                
                
    
    
    print("NIC CARD ADDED")
