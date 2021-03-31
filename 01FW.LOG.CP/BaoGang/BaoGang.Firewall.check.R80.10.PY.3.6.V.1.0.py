# BaoGang.Firewall.check.list.PY.36.V.3.0.py write by python 3.6
import csv
import IPy
import time
import xlwt

# set the log file and dir
log_file = "SH.BG.CP5600.R80.10.20190618.02.log"
log_dir = "D:\\"


def log_split_to_dict(log_line, dict_map):
    #
    # This log_split_to_dict only for Checkpoint R80.10.
    #
    log_line_split = log_line.split('"')
    data_from_log = log_line_split[7]
    time_from_log = log_line_split[9]
    interface_from_log = log_line_split[11]
    action_from_log = log_line_split[17]
    service_from_log = log_line_split[19]
    source_ip = log_line_split[23]
    destination_ip = log_line_split[25]
    tcp_udp = log_line_split[27]
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
        print("Total ", csv_path, "file len :", csv_lenth)


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
    timestamp1 = time.clock()
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())

    #
    # This module defines all the parameter of saved files.
    #
    file_path = log_dir + log_file
    permit_csv_path = file_path + "." + "permit" + "." + ticks + ".csv"
    deny_csv_path = file_path + "." + "deny" + "." + ticks + ".csv"
    permit_rule_exl_path = file_path + "." + "permit.rule" + "." + ticks + ".xls"
    deny_rule_exl_path = file_path + "." + "deny.rule" + "." + ticks + ".xls"

    #
    # This module open the log_file.
    #
    print("Start to load Log files.")

    open_log_file = open(file_path, 'r')
    all_log_lines = open_log_file.readlines()
    open_log_file.close()

    timestamp2 = time.clock()
    print("Total load Log file time used:           ", timestamp2 - timestamp1)

    #
    # This module write the src and dst ip to a list, and count.
    #
    print("Start to count the src and dst ips.")
    source_ip_list = []
    destination_ip_list = []

    for each_log_line in all_log_lines:
        log_line_split = each_log_line.split('"')
        source_ip = log_line_split[23]
        destination_ip = log_line_split[25]
        if source_ip not in source_ip_list:
            source_ip_list.append(source_ip)
        # if destination_ip not in destination_ip_list:
        #     destination_ip_list.append(destination_ip)
    print("Total source_ip_list len :                       ", len(source_ip_list))
    print("Total destination_ip_list len :                  ", len(destination_ip_list))

    timestamp3 = time.clock()
    print("Total count the src and dst ip used:             ", timestamp3 - timestamp2)

    #
    # This module write the src_dst_port info to a dict_map.
    #
    print("Start to write the src_dst_port info to a dict_map.")
    permit_dict_map = {}
    deny_dict_map = {}
    for each_log_line in all_log_lines:
        if "Accept" in each_log_line:
            if "icmp" not in each_log_line:
                log_split_to_dict(each_log_line, permit_dict_map)
        elif "Drop" in each_log_line:
            if "icmp" not in each_log_line:
                log_split_to_dict(each_log_line, deny_dict_map)
    print("Total permit dict file len :", len(permit_dict_map))
    print("Total deny dict file len :", len(deny_dict_map))

    timestamp4 = time.clock()
    print("Total write the src_dst_port info to a dict_map used:", timestamp4 - timestamp3)

    #
    # This module write_dict_to_csv_file.
    #
    print("Start to write_dict_to_csv_file.")
    write_dict_to_csv_file(permit_dict_map, permit_csv_path)
    write_dict_to_csv_file(deny_dict_map, deny_csv_path)

    timestamp5 = time.clock()
    print("Total write_dict_to_csv_file used:", timestamp5 - timestamp4)

    #
    # This module write every src ip log to a single file.
    #
    print("Start to load csv_log files.")

    open_csv_log_file = open(permit_csv_path, 'r')
    all_csv_log_lines = open_csv_log_file.readlines()
    open_csv_log_file.close()

    timestamp6 = time.clock()
    print("Total load csv_Log file time used:           ", timestamp6 - timestamp5)

    for each_wired_ip_list in source_ip_list:
        log_lists = []
        csv_lenth = 0
        for each_log_line in all_csv_log_lines:
            if each_wired_ip_list in each_log_line:
                log_lists.append(each_log_line)
        # write each_wired_ip_csv_path to each_wired_ip_csv
        each_wired_ip_csv_path = file_path + "." + each_wired_ip_list + "." + "csv"
        with open(each_wired_ip_csv_path, 'w', newline='') as csv_file:
            csv_lenth = 0
            csv_writer = csv.writer(csv_file, delimiter=' ')
            for _ in log_lists:
                csv_writer.writerow(_[:-1])
            csv_lenth = len(log_lists)
            print("Total ", each_wired_ip_list, "file len                   :", csv_lenth)

    timestamp7 = time.clock()
    print("Total write every wired_ip csv_Log file time used:           ", timestamp7 - timestamp6)

    print("Total Time used:", timestamp7 - timestamp1)
