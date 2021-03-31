#!/usr/bin/env python
"""
Written by Kang.Chen
Backup VMs.
"""
import os
import time
import arrow

backup_PSPG_vm_names = ["10.12.11.11.PSPG02"]


def backup_vms(vm_lists, vcenter_server, datacenter_name, datastore_name, resource_pool_name):
    for vm_name in vm_lists:
        timestamp_1 = time.clock()
        backup_time = arrow.now().format("YYYYMM")
        backuped_vm_name = vm_name + "." + backup_time
        backup_cmd0 = "python vmware-pyvmomi-community-samples\\samples\\clone_vm.py"
        backup_cmd = backup_cmd0 + " --host " + vcenter_server \
                     + " --no-ssl" \
                     + " --vm-name " + backuped_vm_name \
                     + " -u " + "vsphere.local\\administrator" \
                     + " -p " "\"AP!?&p@Si$rsP3V|U<Tx\"" \
                     + " --template " + vm_name \
                     + " --datacenter-name " + datacenter_name \
                     + " --datastore-name " + datastore_name \
                     + " --resource-pool " + resource_pool_name
        os.system(backup_cmd)
        timestamp_2 = time.clock()
        print("Finish Backup <<<", vm_name, ">>>, Time use is", timestamp_2 - timestamp_1, "seconds.")


def destroy_old_vm(vm_lists, vcenter_server):
    for vm_name in vm_lists:
        timestamp_1 = time.clock()
        destroy_backup_time = arrow.now().shift(months=-2).format("YYYYMM")
        # destroy_backup_time = arrow.now().format("YYYYMM")
        destroy_vm_name = vm_name + "." + destroy_backup_time
        destroy_cmd0 = "python samples\\destroy_vm.py"
        destroy_cmd = destroy_cmd0 + " -s " + vcenter_server \
                      + " -S " \
                      + " -u " + "vsphere.local\\administrator" \
                      + " -p " "\"AP!?&p@Si$rsP3V|U<Tx\"" \
                      + " -v " + destroy_vm_name
        os.system(destroy_cmd)
        timestamp_2 = time.clock()
        print("Finish destroy <<<", vm_name, ">>>, Time use is", timestamp_2 - timestamp_1, "seconds.")


def main():
    """
    Let's fly
    """
    timestamp0 = time.clock()

    vcenter_CDC_DEV = "10.11.246.3"
    datacenter_CDC_DEV = "CDC"
    datastore_CDC_DEV = "10.11.247.105"
    resource_CDC_DEV = "Backup"

    vcenter_CDC_PRO = "10.11.246.1"
    datacenter_CDC_PRO = "CDC"
    datastore_CDC_PRO = "10.12.246.12"
    resource_CDC_PRO = "Backup"

    vcenter_DLP = "10.11.246.5"
    datacenter_DLP = "DLP"
    datastore_DLP = "10.11.246.55.NFS"
    resource_DLP = "Backup"

    # Begin Backup process.

    # backup_vms(backup_test_vm_names, vcenter_CDC_DEV, datacenter_CDC_DEV, datastore_CDC_DEV, resource_CDC_DEV)
    backup_vms(backup_PSPG_vm_names, vcenter_CDC_PRO, datacenter_CDC_PRO, datastore_CDC_PRO, resource_CDC_PRO)

    # Begin destroy_old_vm process.
    # destroy_old_vm(backup_test_vm_names, vcenter_CDC_DEV)
    destroy_old_vm(backup_PSPG_vm_names, vcenter_CDC_PRO)

    # Just a runtime collection.
    timestamp10 = time.clock()
    print("Finish all Backup Jobs, all time use is ", timestamp10 - timestamp0, " seconds")


# start this thing
if __name__ == "__main__":
    main()
