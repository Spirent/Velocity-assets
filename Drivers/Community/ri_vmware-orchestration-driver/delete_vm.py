#!/usr/bin/env python
# Copyright 2015 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print("there was an error")
            task_done = True



def destroy_vm(si, uuid):

    VM = si.content.searchIndex.FindByUuid(None,uuid,True,False)

    if VM is None:
        raise SystemExit(
            "Unable to locate VirtualMachine for uuid {0}"
            .format(uuid)
            )

    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))
    if format(VM.runtime.powerState) == "poweredOn":
        print("Attempting to power off {0}".format(VM.name))
        task = VM.PowerOffVM_Task()
        wait_for_task(task)
        # tasks.wait_for_tasks(si, [TASK])
        print("{0}".format(task.info.state))

    print("Destroying VM from vSphere.")
    task = VM.Destroy_Task()
    #tasks.wait_for_tasks(si, [TASK])
    wait_for_task(task)
    print("Done.")



