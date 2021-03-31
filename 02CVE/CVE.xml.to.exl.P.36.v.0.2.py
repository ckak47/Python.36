# import xml.etree.ElementTree as ET
import os
import untangle
# import sys, urllib.request
import csv
import time

Timestamp1 = time.clock()
Excelpath = "D:\CNVD.csv"
rootdir = "D:\CNVDDatabase"
xml_list = os.listdir(rootdir)
ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())


def construct_headers():
    return ['CNVD_number', 'bidNumber', 'cveNumber', 'title', 'serverity', 'products', 'isEvent', 'submitTime', 'openTime', 'discovererName', 'referenceLink', 'formalWay', 'description', 'patchName', 'patchDescription']


def construct_rows(lst):
    ret = []
    for item in lst:
        try:
            CNVD_number = item.number.cdata
        except:
            CNVD_number = None
        try:
            bidNumber = item.bids.bid.bidNumber.cdata
        except:
            bidNumber = None
        try:
            cveNumber = item.cves.cve.cveNumber.cdata
        except:
            cveNumber = None
        try:
            title = item.title.cdata
        except:
            title = None
        try:
            serverity = item.serverity.cdata
        except:
            serverity = None
        try:
            A = item.products.product
            product_all = ""
            for i in A:
                product_all = product_all + i.cdata + ','
        except:
            product_all = None
        try:
            isEvent = item.isEvent.cdata
        except:
            isEvent = None
        try:
            submitTime = item.submitTime.cdata
        except:
            submitTime = None
        try:
            openTime = item.openTime.cdata
        except:
            openTime = None
        try:
            discovererName = item.discovererName.cdata
        except:
            discovererName = None
        try:
            referenceLink = item.referenceLink.cdata
        except:
            referenceLink = None
        try:
            formalWay = item.formalWay.cdata
        except:
            formalWay = None
        try:
            description = item.description.cdata
        except:
            description = None
        try:
            patchName = item.patchName.cdata
        except:
            patchName = None
        try:
            patchDescription = item.patchDescription.cdata
        except:
            patchDescription = None

        #print(CNVD_number)
        #print(bidNumber)
        #print(cveNumber)

        _tuple = (CNVD_number, bidNumber, cveNumber, title, serverity, product_all, isEvent, submitTime, openTime, discovererName, referenceLink, formalWay, description, patchName, patchDescription)
        ret.append(_tuple)
    return ret


if __name__ == '__main__':
    for index in range(0, len(xml_list)):
        # print(xml_list[index])
        xmlpath = os.path.join(rootdir, xml_list[index])
        cve = untangle.parse(xmlpath)
        with open("D:\CNVD.csv", "a", newline = '', encoding='utf-8') as resultFile:
            wr = csv.writer(resultFile)
            # wr.writerow(construct_headers())
            for i in cve:
                wr.writerows(construct_rows(i.vulnerabilitys.vulnerability))
    Timestamp2 = time.clock()
    print("Total Time used:", Timestamp2 - Timestamp1)
