import pysphere
from pysphere import VIServer
 
host_ip = "200.200.173.45"
username = "administrator@vsphere.local"
passwd = "admin123."
server_obj  = VIServer()
 
server_obj.connect(host=host_ip,user=username,password=passwd)
# 可以连接esxi主机，也可以连接vcenter
 
# 获取连接的对象类型
print server_obj.get_server_type()
 
 
# 获取esxi的版本信息
print server_obj.get_api_version()
 
 
 
# 获取vcenter下的虚拟机的列表，可以带很多的参数，具体看方法的帮助
vm_list = server_obj.get_registered_vms()
 
 
# 关闭连接
server_obj.disconnect()
 
# 获取虚拟机的状态信息
 
# 通过路径获取vm的实例
vm1 = server_obj.get_vm_by_path()
# 通过名称获取vm的实例
vm1 = server_obj.get_vm_by_name()
 
# 下面就可以获取vm的具体信息
print vm1.get_status()
 
# 返回的状态信息会更快
print vm1.get_status(basic_status=True)
 
 
# 判断虚拟机状态的方法
# print vm1.is_powered_off()
# print vm1.is_powered_on()
# 。。。。。。。。
 
 
# 获取vm的详细信息，他是一个dict
print vm1.get_properties()
 
 
# 获取虚拟机的资源池的名称
print vm1.get_resource_pool_name()
 
 
# 操作虚拟机
vm1.power_off()
vm1.power_on()
vm1.suspend()
 
 
# 让命令在后台运行，也就是异步执行
 
vm1.power_on(sync_run=False)




克隆操作
import pysphere
from pysphere import VIServer
 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
 
host_ip = "200.200.173.45"
username = "administrator@vsphere.local"
passwd = "Admin123."
server_obj = VIServer()
 
 
 
server_obj.connect(host=host_ip, user=username, password=passwd)
clone_vm = server_obj.get_vm_by_name("esx6.5")
# new_vm = clone_vm.clone("new_clone_name")
 
print dir(pysphere)



登陆guest

import pysphere
from pysphere import VIServer
 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
 
host_ip = "200.200.173.45"
username = "administrator@vsphere.local"
passwd = "Admin123."
server_obj = VIServer()
 
 
 
server_obj.connect(host=host_ip, user=username, password=passwd)
clone_vm = server_obj.get_vm_by_name("测试虚拟机")
 
 
# 内部做电源操作，需要虚拟机必须要安装vmtools
# 1、需要登录guest
clone_vm.login_in_guest("administrator","admin123.")
 
clone_vm.shutdown_guest()
clone_vm.reboot_guest()
clone_vm.standby_guest()
#挂起虚拟机
 
# 2、对虚拟机内部的文件和文件夹进行操作
 
# 创建目录
clone_vm.make_directory(path=r"c:\tool\test",create_parents=True)
 
# r的意思是read的意思
# create_parents参数的意思是如果指定path的父目录不存在，是否要创建父目录、
 
 
# 移动目录，如果目的端有相同的目录，则会报错
clone_vm.move_directory(r"c:\tool\test",r"d:\tool\test_bak")
 
# 删除目录
clone_vm.delete_directory()
# recursive,如果是true的，会把子目录和文件都会被删除，如果是false，如果有子目录，或者目录下有文件，删除会报错的
 
 
 
# 列出所有的文件
clone_vm.list_files()
 
# 下载文件
clone_vm.get_file()
 
# 上传文件
clone_vm.send_file()
 
# 移动文件
clone_vm.move_file()
 
# 删除文件
clone_vm.delete_file()
 
# ---------------------------------------------------------------------------------------
# 通过pysphere对操作的系统的进程做操作
clone_vm.start_process()
# 该命令返回的结果就是这个进程的id
# program_path,
# args=None 参数
# cwd=None 程序的工作目录
 
clone_vm.get_environment_variables()
# 获取系统所有的环境变量
 
clone_vm.terminate_process()
# 干掉指定的进程id
 
clone_vm.list_processes()
# 列出虚拟机内部的所有的进程



快照操作
import pysphere
from pysphere import VIServer
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
 
host_ip = "200.200.173.45"
username = "administrator@vsphere.local"
passwd = "Admin123."
server_obj = VIServer()
 
server_obj.connect(host=host_ip, user=username, password=passwd)
# 可以连接esxi主机，也可以连接vcenter
 
# 获取连接的对象类型
print server_obj.get_server_type()
 
# 获取esxi的版本信息
print server_obj.get_api_version()
 
 
vm1 = server_obj.get_vm_by_name()
 
# 回滚快照
 
# 回到当前状态的上一个快照的状态
vm1.revert_to_snapshot()
 
#回到某个快照的的状态，
vm1.revert_to_named_snapshot()
 
 
# 创建快照
vm1.create_snapshot("name", sync_run=True, description=None,memory=True, quiesce=True)
# memory=False 就是不做内存快照
# quiesce=True  只对开机状态安装了vmtools的vm生效，让vmtools去冻结vm的内部的文件，提高快照的准确性
 
 
 
# 删除快照
# 删除当前的快照
vm1.delete_current_snapshot()
 
# 删除指定名称的快照
vm1.delete_named_snapshot()
 
#删除指定路径的快照
vm1.delete_snapshot_by_path()
 
 
# 查看某个虚拟机的快照信息
snap_list = vm1.get_snapshots()
 
 
#还有很多的快照的命令
for i in snap_list:
    print i,i.get_name()
	
	

迁移操作
import pysphere
from pysphere import VIServer
 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
 
host_ip = "200.200.173.45"
username = "administrator@vsphere.local"
passwd = "Admin123."
server_obj = VIServer()
 
 
 
server_obj.connect(host=host_ip, user=username, password=passwd)
clone_vm = server_obj.get_vm_by_name("测试虚拟机")
 
clone_vm.migrate()
 
 
# 只迁移主机
# clone_vm.migrate()
# migrate有个参数叫做host，这个host不是esxi的ip地址，这个值是pysphere自己定义的一个值，需要用下面的方法获取
 
# a = server_obj.get_hosts()
# print a
# {'host-184': '200.200.173.41', 'host-1282': '200.200.173.43', 'host-14': '200.200.173.42'}
 
# 这个host-184、host-1282才是这里的host的值
 
 
# resource_pool的值也pysphere定义的，通过下面的方法获取
# b = server_obj.get_resource_pools()
# print b
 
# {'resgroup-1262': '/Resources/cyr', 'resgroup-24': '/Resources', 'resgroup-1261': '/Resources/tc'}

