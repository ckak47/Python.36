#-*- coding:utf-8 -*-
#!/usr/bin/python

import sys
import csv
import pickle
import os
import os.path
#import xlrd
#import xlwt
import codecs
import code
import csv
import re
import datetime
import time
import sys

if __name__ == '__main__':

    FilePath = "C:\Users\Z003NH3W\Desktop\cp01.log"  # 绝对路径
    fp = open(FilePath, 'r');
    alllines = fp.readlines();
    fp.close();
    count=1
    Firewall_Dic={};
    Firewall_List=[];
    Rule_List=[]
    for eachline in alllines:
        count = count + 1
#        print count
        if (count != 1):
            Firewall_List=eachline.split()
            ######Pre Process######
            #####find string "accept"#####
            #####find string "eth1" "eth2"###
            #####filter "icmp"#####
            if ("Accept" in eachline ):
                    if ("icmp" not in eachline):
                        Eth = (Firewall_List[3])  # eth1
                        Accept = Firewall_List[6]  # Accept
                        Dst_Port = Firewall_List[7]  # Dst Port
                        Src_IP = Firewall_List[9]  # Src IP
                        Dst_IP = Firewall_List[10]  # Dst IP
                        Protocal = Firewall_List[11]  # Protocal
                        Eth = eval(Eth)
                        Accept = eval(Accept)
                        Dst_Port = eval(Dst_Port)
                        Src_IP = eval(Src_IP)
                        Dst_IP = eval(Dst_IP)
                        Protocal = eval(Protocal)
                        NewLine=[Eth,Accept,Src_IP,Dst_IP,Dst_Port,Protocal]
						#                        NewLine=[Eth,Accept,Src_IP,Dst_IP,Dst_Port,Protocal]
                        if NewLine not in Rule_List:
                            Rule_List.append(NewLine)
    #将的字典写入相应的.csv 文件
    CSVPath="D:\Rule2018101505.csv"  # 绝对路径
    csvfile = file(CSVPath, 'wb');
    writer = csv.writer(csvfile, dialect='excel');
#    writer.writerow(["ETH", "Accept","Src_IP","Dst_IP","Dst_Port","Protocal"]);
    for i in Rule_List:
        writer.writerow(i);








#                       print Eth  # eth1
#                       print Accept  # Accept
 #                      print Dst_Port  # Dst Port
 #                      print Src_IP  # Src IP
 #                      print Dst_IP  # Dst IP
 #                      print Protocal  # Protocal


#            Eth=eval(Firewall_List[3])          #eth1
 #           Accept=eval(Firewall_List[6])          #Accept
 #           Dst_Port=eval(Firewall_List[7])         #Dst Port
#            Src_IP=eval(Firewall_List[9])          #Src IP
#            Dst_IP=eval(Firewall_List[10])         #Dst IP
#            Protocal=eval(Firewall_List[11])         #Protocal
"""
                if "dst_port" in eachline:
                    srip = re.search('dst_port=(.+?) ', eachline);
                    if srip:
                        print srip
                        print srip.group(1)
                        DstPort = srip.group(1)
                        if DstPort not in Firewall_List:
                            Firewall_List.append(DstPort)
    print Firewall_List
"""
"""
    for eachline in alllines:
        count = count + 1
        print count
        if "src" in eachline:
            srip = re.search('src=(.+?) ', eachline);
            if  srip:
                print srip
                print srip.group(1)
                IP=srip.group(1)
                if Attacked_IP_Dic.has_key(IP):
                    Attacked_IP_Dic[IP] += 1
                else:
                    Attacked_IP_Dic[IP] = 1



    #将的字典写入相应的.csv 文件
    CSVPath="C:\Users\cdc\Desktop\SEAL Log\SEAL_IP_Count.csv"  # 绝对路径
    csvfile = file(CSVPath, 'wb');
    writer = csv.writer(csvfile, dialect='excel');
    writer.writerow(["Attacked IP", "Counts"]);
    for i in Attacked_IP_Dic.keys():
        writer.writerow([i, Attacked_IP_Dic[i]]);


"""