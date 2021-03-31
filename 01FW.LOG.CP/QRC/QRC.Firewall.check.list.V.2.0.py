# -*- coding:utf-8 -*-
# !/usr/bin/python

# import sys
# import csv
# import pickle
# import os
# import os.path
# import xlrd
# import xlwt
# import codecs
# import code
# import csv
# import re
# import datetime
# import time
# import sys
# import IPy
import csv
import time

if __name__ == '__main__':
    Start = time.clock()
    Timestamp1 = time.clock()
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    LogFile = "QD.QRC.CP5600.R77.30.20181015.log"
    LogDir = "D:\\"
    FilePath = LogDir + LogFile
    CSVPath = LogDir + LogFile + "." + ticks + ".csv"
    fp = open(FilePath, 'r')
    All_lines = fp.readlines()
    fp.close()
    Timestamp2 = time.clock()
    Count = 0
    Firewall_Dic = {}
    Firewall_List = []
    Rule_List = []
    for Each_line in All_lines:
        Count = Count + 1
        # print Count
        if Count != 1:
            if "Accept" in Each_line:
                if "icmp" not in Each_line:
                    Firewall_List = Each_line.split('"', 24)
                    Date = (Firewall_List[3])
                    Time = (Firewall_List[5])
                    Interface = (Firewall_List[7])  # Interface
                    Action = Firewall_List[13]  # Action
                    Service = Firewall_List[15]  # Service
                    Source = Firewall_List[19]  # Src IP
                    Destination = Firewall_List[21]  # Dst IP
                    Protocal = Firewall_List[23]  # Protocal
                    Date_Time = Date + " " + Time
                    NewLine = [Interface, Action, Source, Destination, Service, Protocal]
                    NewLine = tuple(NewLine)
                    Firewall_Dic[NewLine] = Date_Time
    Timestamp3 = time.clock()
    CSVfile = open(CSVPath, 'w')
    writer = csv.writer(CSVfile, dialect='excel')
    writer.writerows(["Interface", "Action", "Source", "Destination", "Service", "Protocal", "Date"])
    for i in Firewall_Dic.keys():
        RuleCounts = Firewall_Dic[i]
        RuleCounts = str(RuleCounts)
        j = list(i)
        j.append(RuleCounts)
        writer.writerow(j)

    Time_Range = (time.clock() - Start)
    Timestamp4 = time.clock()

    print("Total Read Log file Time used:", Timestamp2 - Timestamp1)
    print("Total Put in dirt time is:", Timestamp3 - Timestamp2)
    print("Total Write csv Time is:", Timestamp4 - Timestamp3)
    print("Total Time used:", Time_Range)
