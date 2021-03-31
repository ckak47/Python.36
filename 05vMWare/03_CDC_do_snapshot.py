#!/usr/bin/env python
"""

Written by Kang.Chen
Backup VMs.

"""
import atexit
import ssl
import arrow

from pyVmomi import vim, vmodl
from pyVim.task import WaitForTask
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi

dlp_PRO_vm_names = ["139.24.22.236.CNSZH05V236SRV.SGSGPK00V212SRV",
                    "139.24.22.237.CNSZH05V237SRV.SGSGPK00V217SRV",
                    "139.24.22.238.CNSZH05V238SRV.SGSGPK00V219SRV",
                    "139.24.22.239.CNSZH05V239SRV.SGSGPK00V221SRV",
                    "139.24.22.240.CNSZH05V240SRV.SGSGPK0V211SRV"]

vCenter_info = {
    'vcenter_ip': '10.11.246.5',
    'vcenter_password': "AP!?&p@Si$rsP3V|U<Tx",
    'vcenter_user': "vsphere.local\\administrator",
    'ignore_ssl': True
}


def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def list_snapshots_recursively(snapshots):
    snapshot_data = []
    snap_text = ""
    for snapshot in snapshots:
        snap_text = "Name: %s; Description: %s; CreateTime: %s; State: %s" % (
                                        snapshot.name, snapshot.description,
                                        snapshot.createTime, snapshot.state)
        snapshot_data.append(snap_text)
        snapshot_data = snapshot_data + list_snapshots_recursively(
                                        snapshot.childSnapshotList)
    return snapshot_data


def get_snapshots_by_name_recursively(snapshots, snapname):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.name == snapname:
            snap_obj.append(snapshot)
        else:
            snap_obj = snap_obj + get_snapshots_by_name_recursively(
                                    snapshot.childSnapshotList, snapname)
    return snap_obj


def get_current_snap_obj(snapshots, snapob):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.snapshot == snapob:
            snap_obj.append(snapshot)
        snap_obj = snap_obj + get_current_snap_obj(
                                snapshot.childSnapshotList, snapob)
    return snap_obj


def main():

    si = None

    print("Trying to connect to VCENTER SERVER . . .")

    context = None
    if vCenter_info['ignore_ssl'] and hasattr(ssl, "_create_unverified_context"):
        context = ssl._create_unverified_context()

    si = connect.Connect(vCenter_info['vcenter_ip'],
                         443,
                         vCenter_info['vcenter_user'],
                         vCenter_info['vcenter_password'],
                         sslContext=context)

    atexit.register(Disconnect, si)

    print("Connected to VCENTER SERVER !")

    content = si.RetrieveContent()

    backup_time = arrow.now().format("YYYYMMDD")

    for dlp_PRO_vm_name in dlp_PRO_vm_names:
        # snapshot_name = dlp_PRO_vm_name + backup_time
        inputs = {
            'vm_name': dlp_PRO_vm_name,
            # operation in 'create/remove/revert/list_all/list_current/remove_all'
            #
            'operation': 'list_all',
            'snapshot_name': backup_time,
            'ignore_ssl': True
        }

        operation = inputs['operation']
        vm_name = inputs['vm_name']

        vm = get_obj(content, [vim.VirtualMachine], vm_name)

        if not vm:
            print("Virtual Machine %s doesn't exists" % vm_name)
            # sys.exit()
            continue

        if operation != 'create' and vm.snapshot is None:
            print("Virtual Machine %s doesn't have any snapshots" % vm.name)
            # sys.exit()
            continue

        if operation == 'create':
            snapshot_name = inputs['snapshot_name']
            description = "Snapshot for patch"
            dumpMemory = False
            quiesce = False

            print("Creating snapshot %s for virtual machine %s" % (
                snapshot_name, vm.name))
            WaitForTask(vm.CreateSnapshot(
                snapshot_name, description, dumpMemory, quiesce))

        elif operation in ['remove', 'revert']:
            snapshot_name = inputs['snapshot_name']
            snap_obj = get_snapshots_by_name_recursively(
                vm.snapshot.rootSnapshotList, snapshot_name)
            # if len(snap_obj) is 0; then no snapshots with specified name
            if len(snap_obj) == 1:
                snap_obj = snap_obj[0].snapshot
                if operation == 'remove':
                    print("Removing snapshot %s" % snapshot_name)
                    WaitForTask(snap_obj.RemoveSnapshot_Task(True))
                else:
                    print("Reverting to snapshot %s" % snapshot_name)
                    WaitForTask(snap_obj.RevertToSnapshot_Task())
            else:
                print("No snapshots found with name: %s on VM: %s" % (
                    snapshot_name, vm.name))

        elif operation == 'list_all':
            print("Display list of snapshots on virtual machine %s" % vm.name)
            snapshot_paths = list_snapshots_recursively(
                vm.snapshot.rootSnapshotList)
            for snapshot in snapshot_paths:
                print(snapshot)

        elif operation == 'list_current':
            current_snapref = vm.snapshot.currentSnapshot
            current_snap_obj = get_current_snap_obj(
                vm.snapshot.rootSnapshotList, current_snapref)
            current_snapshot = "Name: %s; Description: %s; " \
                               "CreateTime: %s; State: %s" % (
                                   current_snap_obj[0].name,
                                   current_snap_obj[0].description,
                                   current_snap_obj[0].createTime,
                                   current_snap_obj[0].state)
            print("Virtual machine %s current snapshot is:" % vm.name)
            print(current_snapshot)

        elif operation == 'remove_all':
            print("Removing all snapshots for virtual machine %s" % vm.name)
            WaitForTask(vm.RemoveAllSnapshots())

        else:
            print("Specify operation in "
                  "create/remove/revert/list_all/list_current/remove_all")


# Start program
if __name__ == "__main__":
    main()
