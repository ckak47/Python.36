# QRC.Firewall.check.list.PY.36.V.3.0.py write by python 3.6
import csv
import IPy
import time
import xlwt


# start time stamp
timestamp1 = time.clock()

def write_to_sheets(R, List, Sheet_Name):
    for Colum in range(len(List)):
        Sheet_Name.write(R, Colum, List[Colum])

# set the log file and dir
log_file = "20190305-01.txt"
log_dir = "D:\\"

# set the subnets
SubNet_List = ["10.11.104.0/24",
               "10.11.105.0/24",
               "10.12.0.0/16",
               "10.11.128.0/19"]

# set the subnets
# SubNet_List = ["10.11.0.0/16",
#                "10.2.0.0/16",
#                "192.168.2.0/24",
#                "192.168.200.0/24",
#                "192.168.100.0/24",
#                "10.12.0.0/16"]

# set time variable in file_names
ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())

file_path = log_dir + log_file
permit_CSV_path = log_dir + log_file + "." + "permit" + "." + ticks + ".csv"
deny_CSV_path = log_dir + log_file + "." + "deny" + "." + ticks + ".csv"
permit_rule_exl_path = log_dir + log_file + "." + "permit.rule" + "." + ticks + ".xls"
deny_rule_exl_path = log_dir + log_file + "." + "deny.rule" + "." + ticks + ".xls"

# open log file
open_log_file = open(file_path, 'r')
all_log_lines = open_log_file.readlines()
open_log_file.close()

# read log file time.
timestamp2 = time.clock()

if __name__ == '__main__':
    # set permit and deny logs dic:
    # split the log file to a list

    # all_permit_logs = set()
    # all_deny_logs = set()
    permit_map = {}
    deny_map = {}
    for each_log_line in all_log_lines:
        if "Accept" in each_log_line:
            if "icmp" not in each_log_line:
                # split the line:
                firewall_list = each_log_line.split('"', 24)
                Date = (firewall_list[3])
                Time = (firewall_list[5])
                Interface = (firewall_list[7])  # Interface
                Action = firewall_list[13]  # Action
                Service = firewall_list[15]  # Service
                Source = firewall_list[19]  # Src IP
                Destination = firewall_list[21]  # Dst IP
                Protocal = firewall_list[23]  # Protocal
                Date_Time = Date + " " + Time
                permit_log = (Interface, Action, Source, Destination, Service, Protocal)
                if permit_log not in permit_map.keys():
                    permit_date_val = {
                        "start": Date_Time,
                        "end": Date_Time,
                    }
                    permit_map[permit_log] = permit_date_val
                else:
                    permit_map[permit_log]["end"] = Date_Time
        elif "Drop" in each_log_line:
            if "icmp" not in each_log_line:
                # split the line:
                firewall_list = each_log_line.split('"', 24)
                Date = (firewall_list[3])
                Time = (firewall_list[5])
                Interface = (firewall_list[7])  # Interface
                Action = firewall_list[13]  # Action
                Service = firewall_list[15]  # Service
                Source = firewall_list[19]  # Src IP
                Destination = firewall_list[21]  # Dst IP
                Protocal = firewall_list[23]  # Protocal
                Date_Time = Date + " " + Time
                deny_logs = (Interface, Action, Source, Destination, Service, Protocal)
                if deny_logs not in permit_map.keys():
                    deny_date_val = {
                        "start": Date_Time,
                        "end": Date_Time,
                    }
                    deny_map[deny_logs] = deny_date_val
                else:
                    deny_map[deny_logs]["end"] = Date_Time

    print("Total permit Log file len :", len(permit_map))
    print("Total deny Log file len :", len(deny_map))

    # split log time.
    timestamp3 = time.clock()

    all_permit_logs_list = []
    for k, v in permit_map.items():
        permit_tmp = []
        for _ in k:
            permit_tmp.append(_)
        for j in v.values():
            permit_tmp.append(j)
        all_permit_logs_list.append(permit_tmp)

    all_deny_logs_list = []
    for k, v in deny_map.items():
        deny_tmp = []
        for _ in k:
            deny_tmp.append(_)
        for j in v.values():
            deny_tmp.append(j)
        all_deny_logs_list.append(deny_tmp)

    with open(permit_CSV_path, 'w', newline='') as permit_CSV_file:
        permit_writer = csv.writer(permit_CSV_file)
        permit_writer.writerow(['Interface',
                                'Action', 'Source', 'Destination', 'Service', 'Protocal', 'first_Date', 'last_Date'])
        for permit_rows in all_permit_logs_list:
            try:
                IPy.IP(permit_rows[2]) and IPy.IP(permit_rows[3])
                permit_writer.writerow(permit_rows)
            except Exception as e:
                pass
    with open(deny_CSV_path, 'w', newline='') as deny_CSV_file:
        deny_writer = csv.writer(deny_CSV_file)
        deny_writer.writerow(['Interface',
                              'Action', 'Source', 'Destination', 'Service', 'Protocal', 'first_Date', 'last_Date'])
        for deny_rows in all_deny_logs_list:
            try:
                IPy.IP(deny_rows[2]) and IPy.IP(deny_rows[3])
                deny_writer.writerow(deny_rows)
            except Exception as e:
                pass
    timestamp4 = time.clock()

    open_permit_CSV_path = open(permit_CSV_path, 'r')
    all_permit_lines = open_permit_CSV_path.readlines()
    permit_excel = xlwt.Workbook(encoding='utf-8')

    for subnet01 in SubNet_List:
        for subnet02 in SubNet_List:
            if (subnet01 != subnet02):
                RuleList = []
                Count = 0
                for eachline in all_permit_lines:
                    if (Count == 0):
                        Title = eachline.split(",")
                        Count += 1
                    else:
                        eachlist = eachline.split(",")
                        Src_IP = eachlist[2]  # Src IP
                        Dst_IP = eachlist[3]  # Dst IP
                        if (Src_IP in IPy.IP(subnet01) and Dst_IP in IPy.IP(subnet02)):
                            RuleList.append(eachlist)
                            Count += 1
                if (RuleList):
                    SheetName = subnet01.split("/")[0] + " to " + subnet02.split("/")[0]
                    SheetName = str(SheetName)
                    mysheet = permit_excel.add_sheet(SheetName)
                    write_to_sheets(0, Title, mysheet)
                    for i in range(len(RuleList)):
                        write_to_sheets(i + 1, RuleList[i], mysheet)
    OtherList = []
    Flag = 0
    for eachline in all_permit_lines:
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
                    flag01 = 1
                if (Dst_IP in IPy.IP(SubNet)):
                    flag02 = 1
            if (flag01 == 0 or flag02 == 0):
                OtherList.append(eachlist)
    Other_SheetName = "Others"
    Other_sheet = permit_excel.add_sheet(Other_SheetName)
    write_to_sheets(0, Title, Other_sheet)
    for i in range(len(OtherList)):
        write_to_sheets(i + 1, OtherList[i], Other_sheet)
    permit_excel.save(permit_rule_exl_path)

    timestamp5 = time.clock()

    open_deny_CSV_path = open(deny_CSV_path, 'r')
    all_deny_lines = open_deny_CSV_path.readlines()
    deny_excel = xlwt.Workbook(encoding='utf-8')

    for subnet01 in SubNet_List:
        for subnet02 in SubNet_List:
            if (subnet01 != subnet02):
                RuleList = []
                Count = 0
                for eachline in all_deny_lines:
                    if (Count == 0):
                        Title = eachline.split(",")
                        Count += 1
                    else:
                        eachlist = eachline.split(",")
                        Src_IP = eachlist[2]  # Src IP
                        Dst_IP = eachlist[3]  # Dst IP
                        if (Src_IP in IPy.IP(subnet01) and Dst_IP in IPy.IP(subnet02)):
                            RuleList.append(eachlist)
                            Count += 1
                if (RuleList):
                    SheetName = subnet01.split("/")[0] + " to " + subnet02.split("/")[0]
                    SheetName = str(SheetName)
                    mysheet = deny_excel.add_sheet(SheetName)
                    write_to_sheets(0, Title, mysheet)
                    for i in range(len(RuleList)):
                        write_to_sheets(i + 1, RuleList[i], mysheet)
    OtherList = []
    Flag = 0
    for eachline in all_deny_lines:
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
                    flag01 = 1
                if (Dst_IP in IPy.IP(SubNet)):
                    flag02 = 1
            if (flag01 == 0 or flag02 == 0):
                OtherList.append(eachlist)
    Other_SheetName = "Others"
    Other_sheet = deny_excel.add_sheet(Other_SheetName)
    write_to_sheets(0, Title, Other_sheet)
    for i in range(len(OtherList)):
        write_to_sheets(i + 1, OtherList[i], Other_sheet)
    deny_excel.save(deny_rule_exl_path)

    timestamp6 = time.clock()
    print("Total Read Log file Time used:", timestamp2 - timestamp1)
    print("Total Put in list time is:", timestamp3 - timestamp2)
    print("Total Write csv Time is:", timestamp4 - timestamp3)
    print("Total Write permit rule Time is:", timestamp5 - timestamp4)
    print("Total Write deny rule Time is:", timestamp6 - timestamp5)
    print("Total Time used:", timestamp6 - timestamp1)

