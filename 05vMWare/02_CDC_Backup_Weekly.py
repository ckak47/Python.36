#!/usr/bin python3
"""
Written by Kang.Chen
Backup VMs.
"""
import os
import datetime
import arrow

backup_CDC_vm_names = ["CDC-Gerrit-Server.10.11.63.162",
                       "CDC-Gerrit-CodeReview-Collect.10.11.63.167"]
backup_CDC_PRO_vm_names = ["10.11.148.11.JIRA",
                           "10.11.148.12.WiKi"]


def backup_vms(vm_lists, vcenter_server, datacenter_name, datastore_name, resource_pool_name):
    for vm_name in vm_lists:
        # timestamp_1 = datetime.datetime.now()
        timestamp_1 = datetime.datetime.now()
        backup_time = arrow.now().format("W")[0:8]
        backuped_vm_name = vm_name + "." + backup_time
        backup_cmd0 = "python samples\\clone_vm.py"
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
        timestamp_2 = datetime.datetime.now()
        print("Finish Backup <<<", vm_name, ">>>, Time use is", timestamp_2 - timestamp_1)


def destroy_old_vm(vm_lists, vcenter_server):
    for vm_name in vm_lists:
        timestamp_1 = datetime.datetime.now()
        destroy_backup_time = arrow.now().shift(weeks=-4).format("W")[0:8]
        destroy_vm_name = vm_name + "." + destroy_backup_time
        destroy_cmd0 = "python samples\\destroy_vm.py"
        destroy_cmd = destroy_cmd0 + " -s " + vcenter_server \
                      + " -S " \
                      + " -u " + "vsphere.local\\administrator" \
                      + " -p " "\"AP!?&p@Si$rsP3V|U<Tx\"" \
                      + " -v " + destroy_vm_name
        os.system(destroy_cmd)
        timestamp_2 = datetime.datetime.now()
        print("Finish destroy <<<", destroy_vm_name, ">>>, Time use is", timestamp_2 - timestamp_1)


def main():
    """
    Let's fly
    """
    timestamp0 = datetime.datetime.now()

    vcenter_CDC_DEV = "10.11.246.3"
    datacenter_CDC_DEV = "DEV"
    datastore_CDC_DEV = "CNSZ01"
    resource_CDC_DEV = "Backup"

    vcenter_CDC_PRO = "10.11.246.1"
    datacenter_CDC_PRO = "PRO"
    datastore_CDC_PRO = "CNSZ01"
    resource_CDC_PRO = "CDC.Backup"

    # Begin Backup process.
    backup_vms(backup_CDC_vm_names, vcenter_CDC_DEV, datacenter_CDC_DEV, datastore_CDC_DEV, resource_CDC_DEV)
    backup_vms(backup_CDC_PRO_vm_names, vcenter_CDC_PRO, datacenter_CDC_PRO, datastore_CDC_PRO, resource_CDC_PRO)

    # Begin destroy_old_vm process.
    destroy_old_vm(backup_CDC_vm_names, vcenter_CDC_DEV)
    destroy_old_vm(backup_CDC_PRO_vm_names, vcenter_CDC_PRO)

    # Just a runtime collection.
    timestamp10 = datetime.datetime.now()
    print("Finish all Backup Jobs, all time use is ", timestamp10 - timestamp0)


# start this thing
if __name__ == "__main__":
    main()
