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
    FilePath = "C:\Users\Z003NH3W\Desktop\cp.log.test.01"  # 绝对路径
    fp = open(FilePath, 'r')
    alllines = fp.readlines()
    fp.close()
    #count = 1
    Firewall_Dic = {}
    Firewall_List = []
    Rule_List = []
    for eachline in alllines:
        Firewall_List = eachline.split('"')
        print Firewall_List

'''

    for eachline in alllines:
        #count = count + 1
        #print count
        if (count != 1):
            Firewall_List = eachline.split()
            print Firewall_List
            print count
'''
