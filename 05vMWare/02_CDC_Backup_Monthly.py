#!/usr/bin python3
"""
Written by Kang.Chen
Backup VMs.
"""
import os
import datetime
import arrow

backup_test_vm_names = ["10.11.34.1.C7.mini.200G"]
backup_DLP_DMZ_vm_names = ["10.11.116.11.CNSZH05V201SRV"]
backup_DLP_PRO_vm_names = ["139.24.22.234.CNSZH05V234X.SGSGPK0V204X",
                           "139.24.22.236.CNSZH05V236SRV.SGSGPK00V212SRV",
                           "139.24.22.237.CNSZH05V237SRV.SGSGPK00V217SRV",
                           "139.24.22.238.CNSZH05V238SRV.SGSGPK00V219SRV",
                           "139.24.22.239.CNSZH05V239SRV.SGSGPK00V221SRV",
                           "139.24.22.240.CNSZH05V240SRV.SGSGPK0V211SRV"]
backup_CDC_vm_names = ["CDC-Gerrit-Server.10.11.63.162",
                       "CDC-Jenkins-Server.10.11.63.163",
                       "CDC-SonarQube5-Server.10.11.63.164",
                       "CDC-Artifact-Server.10.11.63.165",
                       "CDC-SonarQube6-Server.10.11.63.166",
                       "CDC-Gerrit-CodeReview-Collect.10.11.63.167",
                       "10.11.34.13.IPsec02",
                       "10.11.16.41.CounterACT",
                       "10.11.16.200-AD.DNS.NTP.-Win2012",
                       "10.11.16.33.Zabbix.4.0.1"]
backup_CDC_DMZ_vm_names = ["10.11.104.07.Logstash.agg.SEAL",
                           "10.11.104.08.Logstash.agg.SEWC",
                           "10.11.104.09.Logstash.agg.SSCL",
                           "10.11.104.10.Logstash.SMVS",
                           "10.11.104.13.ESM.Console",
                           "10.11.104.22.Nginx.jira",
                           "10.11.104.24.Nginx.dlp",
                           "10.11.104.25.Nginx.Monitor",
                           "10.11.104.26.Nginx.ESM",
                           "10.11.104.27.Nginx.CJH",
                           "10.11.104.42.Kali-x64-nessus",
                           "10.11.104.61.Logstash.AWS",
                           "10.11.104.62.Logstash.PSPG",
                           "10.11.105.11.CDC-Nexus-Server1",
                           "10.11.105.22.CDC.OfficeScanServer",
                           "10.11.105.27.Win2019.WSUS.DLP",
                           "10.11.105.31.Win2008R2",
                           "10.11.105.41.IPGuard",
                           "10.11.105.51.OSA_Licenser",
                           "10.11.105.201.DNS.NTP",
                           "10.11.105.202.DNS.NTP",
                           "10.11.105.208.C7.LDAP.Mail",
                           "10.11.106.11.Gitlab",
                           "10.11.106.12.Samba",
                           "10.11.107.11.Squid.Proxy",
                           "10.11.107.201.DNS.NTP",
                           "10.11.117.12.Win.2019.WSUS.BYC"]
backup_CDC_PRO_vm_names = ["10.11.148.11.JIRA",
                           "10.11.148.12.WiKi",
                           "10.11.148.13.MySQL10T",
                           "10.11.148.21.JIRA.WiKi.All",
                           "10.11.160.211.Allen.Storage(20T)",
                           "10.11.246.1-PRO-vCenter",
                           "10.11.246.3-DEV-vCenter",
                           "10.11.246.5.PG01.vCenter"]
backup_CDC_DEMO_vm_names = ["10.11.100.71-kafka01",
                            "10.11.100.72-ELasticSearch01",
                            "10.11.100.73-MongoDB01",
                            "10.11.100.74-SI-SIEM",
                            "10.11.100.75-MySQL",
                            "10.11.100.76-Redis",
                            "10.11.100.77-MicroServices",
                            "10.11.100.78-WebServer"]
backup_PSPG_vm_names = ["10.12.11.11.PSPG02"]


def backup_vms(vm_lists, vcenter_server, datacenter_name, datastore_name, resource_pool_name):
    for vm_name in vm_lists:
        # timestamp_1 = datetime.datetime.now()
        timestamp_1 = datetime.datetime.now()
        backup_time = arrow.now().format("YYYYMM")
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
    datastore_PG_PRO = "10.12.246.12"
    resource_CDC_PRO = "CDC.Backup"
    resource_PG_PRO = "Backup"

    vcenter_DLP = "10.11.246.5"
    datacenter_DLP = "DLP"
    datastore_DLP = "10.11.246.55.NFS"
    resource_DLP = "Backup"

    # Begin Backup process.
    backup_vms(backup_DLP_DMZ_vm_names, vcenter_CDC_DEV, datacenter_CDC_DEV, datastore_CDC_DEV, resource_CDC_DEV)
    backup_vms(backup_DLP_PRO_vm_names, vcenter_DLP, datacenter_DLP, datastore_DLP, resource_DLP)
    backup_vms(backup_CDC_vm_names, vcenter_CDC_DEV, datacenter_CDC_DEV, datastore_CDC_DEV, resource_CDC_DEV)
    backup_vms(backup_CDC_DMZ_vm_names, vcenter_CDC_DEV, datacenter_CDC_DEV, datastore_CDC_DEV, resource_CDC_DEV)
    backup_vms(backup_CDC_PRO_vm_names, vcenter_CDC_PRO, datacenter_CDC_PRO, datastore_CDC_PRO, resource_CDC_PRO)
    backup_vms(backup_CDC_DEMO_vm_names, vcenter_CDC_DEV, datacenter_CDC_DEV, datastore_CDC_DEV, resource_CDC_DEV)
    backup_vms(backup_PSPG_vm_names, vcenter_CDC_PRO, datacenter_CDC_PRO, datastore_PG_PRO, resource_PG_PRO)

    # Begin destroy_old_vm process.
    destroy_old_vm(backup_DLP_DMZ_vm_names, vcenter_CDC_DEV)
    destroy_old_vm(backup_DLP_PRO_vm_names, vcenter_DLP)
    destroy_old_vm(backup_CDC_vm_names, vcenter_CDC_DEV)
    destroy_old_vm(backup_CDC_DMZ_vm_names, vcenter_CDC_DEV)
    destroy_old_vm(backup_CDC_PRO_vm_names, vcenter_CDC_DEV)
    destroy_old_vm(backup_CDC_DEMO_vm_names, vcenter_CDC_DEV)
    destroy_old_vm(backup_PSPG_vm_names, vcenter_CDC_PRO)

    # Just a runtime collection.
    timestamp10 = datetime.datetime.now()
    print("Finish all Backup Jobs, all time use is ", timestamp10 - timestamp0)


# start this thing
if __name__ == "__main__":
    main()
