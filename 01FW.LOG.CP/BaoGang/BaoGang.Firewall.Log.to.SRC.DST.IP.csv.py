# Firewall.check.list.PY.36.V.3.0.py write by python 3.6
import csv
import IPy
import time
import xlwt

# start time stamp
timestamp1 = time.clock()

# set the log file and dir
log_file = "SH.BG.CP5600.R80.10.20190619.log"
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


def write_list_to_csv_file(ip_list, csv_path):
    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=' ')
        for _ in ip_list:
            csv_writer.writerow(_)


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
    # set time variable used in file_names
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    file_path = log_dir + log_file

    # This module open the log_file as a list.
    open_log_file = open(file_path, 'r')
    all_log_lines = open_log_file.readlines()
    open_log_file.close()
    timestamp2 = time.clock()

    # timestamp2 - timestamp1 = read log_file time.
    print("Total Read Log file Time used:", timestamp2 - timestamp1)
    permit_source_ip_list = []
    permit_destination_ip_list = []
    deny_source_ip_list = []
    deny_destination_ip_list = []
    for each_log_line in all_log_lines:
        if "Accept" in each_log_line:
            log_line_split = each_log_line.split('"')
            source_ip = log_line_split[23]
            destination_ip = log_line_split[25]
            if source_ip not in permit_source_ip_list:
                permit_source_ip_list.append(source_ip)
            # if destination_ip not in permit_destination_ip_list:
            #     permit_destination_ip_list.append(destination_ip)
        elif "Drop" in each_log_line:
            log_line_split = each_log_line.split('"')
            source_ip = log_line_split[23]
            destination_ip = log_line_split[25]
            if source_ip not in deny_source_ip_list:
                deny_source_ip_list.append(source_ip)
            # if destination_ip not in deny_destination_ip_list:
            #     deny_destination_ip_list.append(destination_ip)

    print("Total permit_source_ip_list len :        ", len(permit_source_ip_list))
    print("Total permit_destination_ip_list len :   ", len(permit_destination_ip_list))
    print("Total deny_source_ip_list len :          ", len(deny_source_ip_list))
    print("Total deny_destination_ip_list len :     ", len(deny_destination_ip_list))
    timestamp3 = time.clock()

    # timestamp3 - timestamp2 = split log time.
    print("Total Split Log file Time used:", timestamp3 - timestamp2)

    # write_dict_to_csv_file
    permit_source_ip_list_path = file_path + "." + "permit_source_ip" + "." + ticks + ".csv"
    # permit_destination_ip_list_path = file_path + "." + "permit_destination_ip" + "." + ticks + ".csv"
    deny_source_ip_list_path = file_path + "." + "deny_source_ip" + "." + ticks + ".csv"
    # deny_destination_ip_list_path = file_path + "." + "deny_destination_ip" + "." + ticks + ".csv"

    # write_list_to_csv_file(permit_source_ip_list, permit_source_ip_list_path)
    # # write_list_to_csv_file(permit_destination_ip_list, permit_destination_ip_list_path)
    # write_list_to_csv_file(deny_source_ip_list, deny_source_ip_list_path)
    # # write_list_to_csv_file(deny_destination_ip_list, deny_destination_ip_list_path)

    timestamp4 = time.clock()

    for each_wired_ip_list in permit_source_ip_list:
        log_lists = []
        csv_lenth = 0
        for each_log_line in all_log_lines:
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
            print("Total ", each_wired_ip_csv_path, "file len                   :", csv_lenth)

    timestamp5 = time.clock()

    # timestamp5 - timestamp4 = write permit_excel time.
    # print("Total Write rule_file Time is:", timestamp5 - timestamp4)
    print("Total Time used:", timestamp5 - timestamp1)

