#-*- coding:utf-8 -*-
#!/usr/bin/python

#import sys
#import csv
#import pickle
#import os
#import os.path
#import xlrd
#import xlwt
#import codecs
#import code
#import csv
#import re
#import datetime
#import time
#import sys
#import IPy
import csv
import time

if __name__ == '__main__':
    start=time.clock()
    FilePath = "D:\SZ.CDC.CP5600.R77.30.fw.all.log"  # 绝对路径
    CSVPath="D:\SZ.CDC.CP5600.R77.30.fw.all.log.csv"    # 绝对路径
    fp = open(FilePath, 'r');
    alllines = fp.readlines();
    fp.close();
    count=0
    Firewall_Dic={};
    Firewall_List=[];
    Rule_List=[]
    for eachline in alllines:
        count = count + 1
        print count
        if (count != 1):
            if ("Accept" in eachline ):
                    if ("icmp" not in eachline):
                        Firewall_List = eachline.split()
                        Date=(Firewall_List[1])
                        Time=(Firewall_List[2])
                        Eth = (Firewall_List[3])  # eth1
                        Accept = Firewall_List[6]  # Accept
                        Dst_Port = Firewall_List[7]  # Dst Port
                        Src_IP = Firewall_List[9]  # Src IP
                        Dst_IP = Firewall_List[10]  # Dst IP
                        Protocal = Firewall_List[11]  # Protocal

                        Date=eval(Date)
                        Time=eval(Time)
                        Eth = eval(Eth)
                        Accept = eval(Accept)
                        Dst_Port = eval(Dst_Port)
                        Src_IP = eval(Src_IP)
                        Dst_IP = eval(Dst_IP)
                        Protocal = eval(Protocal)

                        Date_Time=Date+" "+Time

                        NewLine=[Eth,Accept,Src_IP,Dst_IP,Dst_Port,Protocal]
                        NewLine=tuple(NewLine)

                        Firewall_Dic[NewLine]=Date_Time
    #CSVPath="D:\SZ.CDC.CP5600.R77.30.fw.all.log.csv"    # 绝对路径
    #将的字典写入相应的.csv 文件
    csvfile = file(CSVPath, 'wb');
    writer = csv.writer(csvfile, dialect='excel');
    writer.writerow(["Interface", "Action","Source","Destination","Service","Protocal","Date"]);
    for i in Firewall_Dic.keys():
        RuleCounts=Firewall_Dic[i]
        RuleCounts=str(RuleCounts)
        j=list(i)
        j.append(RuleCounts)
        writer.writerow(j);

    elapsed=(time.clock()-start)
    print("Time used:",elapsed)


