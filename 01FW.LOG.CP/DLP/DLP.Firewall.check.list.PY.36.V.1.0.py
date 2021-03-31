# Firewall.check.list.PY.36.V.3.0.py write with python 3.6
import csv
import IPy
import time
import xlwt
import os

# set the log file and dir
log_dir = "C:\\Users\\Z003NH3W\\Desktop\\Log.FW.DLP.CP5100\\"


server_ip = ["139.24.22.234",
             "139.24.22.235",
             "139.24.22.236",
             "139.24.22.237",
             "139.24.22.238",
             "139.24.22.239",
             "139.24.22.240"]


def log_split_to_dict(log_line, dict_map):
    #
    # This log_split_to_dict only for Checkpoint R80.10 through "fwm logexport".
    #
    log_line_split = log_line.split(';')
    data_from_log = log_line_split[1]
    time_from_log = log_line_split[2]
    interface_from_log = log_line_split[7]
    action_from_log = log_line_split[5]
    service_from_log = log_line_split[29]
    source_ip = log_line_split[19]
    destination_ip = log_line_split[20]
    tcp_udp = log_line_split[21]
    data_and_time = data_from_log + " " + time_from_log
    new_log = (interface_from_log, action_from_log, source_ip, destination_ip, service_from_log, tcp_udp)
    if new_log not in dict_map.keys():
        set_data_and_time_val = {
            "start": data_and_time,
            "end": data_and_time,
        }
        dict_map[new_log] = set_data_and_time_val
    else:
        dict_map[new_log]["end"] = data_and_time


def write_dict_to_csv_file(dict_map, csv_path):
    with open(csv_path, 'w', newline='') as csv_file:
        csv_lenth = 0
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['interface',
                             'action',
                             'source',
                             'destination',
                             'service',
                             'tcp_udp',
                             'first_time',
                             'last_time'])
        for k, v in dict_map.items():
            log_lists = []
            for _ in k:
                log_lists.append(_)
            for j in v.values():
                log_lists.append(j)
            try:
                IPy.IP(log_lists[2]) and IPy.IP(log_lists[3])
                csv_writer.writerow(log_lists)
                csv_lenth += 1
            except Exception as e:
                pass
        print(csv_path, "file len :", csv_lenth)


def write_list_to_csv_file(list_name, csv_path):
    with open(csv_path, 'w', newline='') as csv_file:
        csv_lenth = 0
        csv_writer = csv.writer(csv_file)
        for log_lists in list_name:
            csv_writer.writerow(log_lists)
            csv_lenth += 1
        print(csv_path, "file length is :", csv_lenth)


def csv_split_to_sheet(assign_subnets_list, log_lines, exl_name):
    for sub_net_01 in assign_subnets_list:
        for sub_net_02 in assign_subnets_list:
            if sub_net_01 != sub_net_02:
                new_list = []
                count = 0
                title = ['interface', 'action', 'source', 'destination', 'service', 'tcp_udp', 'first_time',
                         'last_time']
                for line in log_lines:
                    if count == 0:
                        #title = line.split(",")
                        count += 1
                    else:
                        line_list = line.split(",")
                        src_ip = line.split(",")[2]  # Src IP
                        dst_ip = line.split(",")[3]  # Dst IP
                        if src_ip in IPy.IP(sub_net_01) and dst_ip in IPy.IP(sub_net_02):
                            new_list.append(line_list)
                            count += 1
                if new_list:
                    sheet_name = str(sub_net_01.split("/")[0] + "-" + sub_net_02.split("/")[0])
                    my_sheet = exl_name.add_sheet(sheet_name)
                    for value in range(len(title)):
                        my_sheet.write(0, value, title[value])
                    rn = 1
                    for row in new_list:
                        cn = 0
                        for _ in range(len(row)):
                            my_sheet.write(rn, cn, row[_])
                            cn += 1
                        rn += 1


def csv_split_to_sheet_for_others(assign_subnets_list, log_lines, exl_name):
    other_list = []
    title_flag = 0
    title = ['interface', 'action', 'source', 'destination', 'service', 'tcp_udp', 'first_time', 'last_time']
    for line in log_lines:
        if title_flag == 0:
            #title = line.split(",")
            title_flag += 1
        else:
            line_list = line.split(",")
            flag_01 = 0
            flag_02 = 0
            src_ip = line_list[2]  # Src IP
            dst_ip = line_list[3]  # Dst IP
            for sub_net in assign_subnets_list:
                if src_ip in IPy.IP(sub_net):
                    flag_01 = 1
                if dst_ip in IPy.IP(sub_net):
                    flag_02 = 1
            if flag_01 == 0 or flag_02 == 0:
                other_list.append(line_list)
    if other_list:
        my_sheet = exl_name.add_sheet("others")
        for value in range(len(title)):
            my_sheet.write(0, value, title[value])
        rn = 1
        for row in other_list:
            cn = 0
            for _ in range(len(row)):
                my_sheet.write(rn, cn, row[_])
                cn += 1
            rn += 1


if __name__ == '__main__':
    # start time stamp
    print("Starting file analysis . . .")
    timestamp1 = time.clock()
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())

    #
    # This module open the log_file.
    # 得到文件夹下的所有文件名称
    files = os.listdir(log_dir)

    permit_dict_map = {}
    deny_dict_map = {}

    # 遍历文件夹
    for file in files:
        # 判断是否是文件夹，不是文件夹才打开
        if not os.path.isdir(file):
            # 打开文件
            open_log_file = open(log_dir + "\\" + file)
            all_log_lines = open_log_file.readlines()
            for each_log_line in all_log_lines:
                if "accept" in each_log_line:
                    if "icmp" not in each_log_line:
                        log_split_to_dict(each_log_line, permit_dict_map)
                elif "drop" in each_log_line:
                    if "icmp" not in each_log_line:
                        log_split_to_dict(each_log_line, deny_dict_map)
            print(log_dir + "\\" + file, "permit len is:     ", len(permit_dict_map))
            print(log_dir + "\\" + file, "deny len is:       ", len(deny_dict_map))

    timestamp2 = time.clock()
    print("Total log split to dict_map used:", timestamp2 - timestamp1, "s")

    #
    # This module write_dict_to_csv_file.
    #
    permit_csv_path = log_dir + "permit" + "." + ticks + ".csv"
    deny_csv_path = log_dir + "deny" + "." + ticks + ".csv"

    print("Start to write_dict_to_csv_file.")
    write_dict_to_csv_file(permit_dict_map, permit_csv_path)
    write_dict_to_csv_file(deny_dict_map, deny_csv_path)

    timestamp3 = time.clock()
    print("Total write dict to csv file used:", timestamp3 - timestamp2, "s")
    print("Total file analysis time is :", timestamp3 - timestamp1, "s")
