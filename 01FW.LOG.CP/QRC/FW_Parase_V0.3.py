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
import xlrd
import xlwt
import IPy


def WriteSheet (R,List,Sheet_Name):
    for Colum in range(len(List)):
        Sheet_Name.write(R, Colum, List[Colum])


if __name__ == '__main__':

    start = time.clock()

    Rule="D:\cp02.csv"    # 绝对路径
    fp = open(Rule, 'r');
    Alllines = fp.readlines();
    fp.close();

    Myexcel = xlwt.Workbook(encoding='utf-8')
    Myexcel_Name="D:\cp01.xls"


#    SubNet_List=["10.11.104.0/24","10.11.105.0/24","10.11.108.0/24","10.11.128.0/24","10.11.130.0/24",
#                "10.11.132.0/24","10.11.134.0/24","10.11.136.0/24","10.11.137.0/24","10.11.160.0/24","10.11.149.0/24"]

    SubNet_List=["10.1.0.0/24","10.12.0.0/16","10.2.0.0/24","169.254.0.0/16","172.20.10.0/24"]


    for subnet01 in SubNet_List:
        for subnet02 in SubNet_List:
            if (subnet01 != subnet02):
                RuleList = []
                Count = 0
                for eachline in Alllines:
                    if (Count==0):
                        Title = eachline.split(",")
                        Count += 1
                    else:
                        eachlist = eachline.split(",")
                        Src_IP = eachlist[2]  # Src IP
                        Dst_IP = eachlist[3]  # Dst IP
                        if (Src_IP in IPy.IP(subnet01) and Dst_IP in IPy.IP(subnet02)):
                            RuleList.append(eachlist)
                            Count += 1
                if(RuleList):
                    SheetName = subnet01.split("/")[0] + " to " + subnet02.split("/")[0]
                    SheetName=str(SheetName)
                    mysheet = Myexcel.add_sheet(SheetName)
                    WriteSheet(0, Title, mysheet)
                    for i in range(len(RuleList)):
                        WriteSheet(i+1,RuleList[i],mysheet)
    OtherList=[]
    Flag=0
    for eachline in Alllines:
        if (Flag == 0):
            Flag += 1
        else:
            eachlist = eachline.split(",")
            flag01 = 0
            flag02 = 0
            Src_IP = eachlist[2]  # Src IP
            Dst_IP = eachlist[3]  # Dst IP
            for SubNet in SubNet_List:
                if (Src_IP in IPy.IP(SubNet)):
                    flag01=1
                if (Dst_IP in IPy.IP(SubNet)):
                    flag02=1
            if(flag01==0 or flag02==0 ):
                OtherList.append(eachlist)
    Other_SheetName="Others"
    Other_sheet = Myexcel.add_sheet(Other_SheetName)
    WriteSheet(0, Title, Other_sheet)
    for i in range(len(OtherList)):
        WriteSheet(i + 1, OtherList[i], Other_sheet)

    Myexcel.save(Myexcel_Name)

    elapsed=(time.clock()-start)
    print("Time used:",elapsed)













