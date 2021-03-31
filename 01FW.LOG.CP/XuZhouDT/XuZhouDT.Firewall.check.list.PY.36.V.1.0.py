# XuZhouDT.Firewall.check.list.PY.36.V.1.0.py write by python 3.6
import csv
import IPy
import time
import xlwt
import pickle
import json

# start time stamp
timestamp1 = time.clock()

# set the log file and dir
log_file = "2019.cp.r80.10.xz.log"
log_dir = "D:\\"


def log_split_to_dict(log_line, new_list):
    #
    # This log_split_to_dict only for Checkpoint R80.10.
    #

    log_line_split = log_line.split(';')

    log_num = log_line_split[0]
    log_date = log_line_split[1]
    log_time = log_line_split[2]
    log_orig = log_line_split[3]
    log_type = log_line_split[4]
    log_action = log_line_split[5]
    log_alert = log_line_split[6]
    log_i_f_name = log_line_split[7]
    log_i_f_dir = log_line_split[8]
    log_product = log_line_split[9]
    log_LogId = log_line_split[10]
    log_ContextNum = log_line_split[11]
    log_origin_id = log_line_split[12]
    log_ContentVersion = log_line_split[13]
    log_HighLevelLogKey = log_line_split[14]
    log_SequenceNum = log_line_split[15]
    log_sys_message = log_line_split[16]
    log_ProductFamily = log_line_split[17]
    log_description = log_line_split[18]
    log_status = log_line_split[19]
    log_version = log_line_split[20]
    log_comment = log_line_split[21]
    log_update_service = log_line_split[22]
    log_reason = log_line_split[23]
    log_Severity = log_line_split[24]
    log_failure_impact = log_line_split[25]
    log_src = log_line_split[26]
    log_dst = log_line_split[27]
    log_proto = log_line_split[28]
    log_message_info = log_line_split[29]
    log_TCP_packet_out_of_state = log_line_split[30]
    log_tcp_flags = log_line_split[31]
    log_service = log_line_split[32]
    log_s_port = log_line_split[33]
    log_fw_message = log_line_split[34]
    log_rule_guid = log_line_split[35]
    log_hit = log_line_split[36]
    log_policy = log_line_split[37]
    log_first_hit_time = log_line_split[38]
    log_last_hit_time = log_line_split[39]
    log_log_id = log_line_split[40]
    log_Internal_CA = log_line_split[41]
    log_serial_num = log_line_split[42]
    log_dn = log_line_split[43]
    log_inzone = log_line_split[44]
    log_outzone = log_line_split[45]
    log_service_id = log_line_split[46]
    # log_UP_match_table_match_id = log_line_split[47]
    # log_UP_match_table_layer_uuid = log_line_split[48]
    # log_UP_match_table_layer_name = log_line_split[49]
    # log_UP_match_table_rule_uid = log_line_split[50]
    # log_UP_match_table_rule_name = log_line_split[51]
    # log_UP_match_table_action = log_line_split[52]
    # log_UP_match_table_parent_rule = log_line_split[53]
    # log_ICMP = log_line_split[54]
    # log_ICMP_Type = log_line_split[55]
    # log_ICMP_Code = log_line_split[56]

    # log_Source_Machine_Name = log_line_split[1]
    # log_Source_User_Name = log_line_split[3]
    # log_Number = log_line_split[5]
    # log_Date = log_line_split[7]
    # log_Time = log_line_split[9]
    # log_Interface = log_line_split[11]
    # log_Origin = log_line_split[13]
    # log_Type = log_line_split[15]
    # log_Action = log_line_split[17]
    # log_Service = log_line_split[19]
    # log_Source_Port = log_line_split[21]
    # log_Source = log_line_split[23]
    # log_Destination = log_line_split[25]
    # log_Protocol = log_line_split[27]
    # log_Rule = log_line_split[29]
    # log_Rule_Name = log_line_split[31]
    # log_Current_Rule_Number = log_line_split[33]
    # log_User = log_line_split[35]
    # log_Information = log_line_split[37]
    # log_Product = log_line_split[39]

    log_data_time = log_date + " " + log_time
    new_log = [log_action, log_src, log_dst, log_proto, log_service, log_data_time]

    new_list.append(new_log)

    # if new_log not in dict_map.keys():
    #     set_data_and_time_val = {
    #         "start": log_data_time,
    #         "end": log_data_time,
    #     }
    #     dict_map[new_log] = set_data_and_time_val
    # else:
    #     dict_map[new_log]["end"] = log_data_time


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
    # set time variable used in file_names
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    file_path = log_dir + log_file
    # permit_csv_path = file_path + "." + "permit" + "." + ticks + ".csv"
    # deny_csv_path = file_path + "." + "deny" + "." + ticks + ".csv"
    # permit_rule_exl_path = file_path + "." + "permit.rule" + "." + ticks + ".xls"
    # deny_rule_exl_path = file_path + "." + "deny.rule" + "." + ticks + ".xls"
    log_files_from_log = file_path + "." + "all.log" + "." + ticks + ".txt"

    # This module open the log_file as a list.
    open_log_file = open(file_path, 'r')
    all_log_lines = open_log_file.readlines()
    open_log_file.close()
    timestamp2 = time.clock()

    # timestamp2 - timestamp1 = read log_file time.
    print("Total Read Log file Time used:", timestamp2 - timestamp1)

    # permit_dict_map = {}
    # deny_dict_map = {}
    new_list_from_log = []

    for each_log_line in all_log_lines:
        log_split_to_dict(each_log_line, new_list_from_log)

    # for each_log_line in all_log_lines:
    #     if "Accept" in each_log_line:
    #         if "icmp" not in each_log_line:
    #             log_split_to_dict(each_log_line, permit_dict_map)
    #     elif "Drop" in each_log_line:
    #         if "icmp" not in each_log_line:
    #             log_split_to_dict(each_log_line, deny_dict_map)
    # print("Total permit dict file len :", len(permit_dict_map))
    # print("Total deny dict file len :", len(deny_dict_map))
    # timestamp3 - timestamp2 = split log time.
    timestamp3 = time.clock()
    print("Total Split Log file Time used:", timestamp3 - timestamp2)

    with open(log_files_from_log, 'w', encoding='utf-8') as f:
        json.dump(new_list_from_log, f, ensure_ascii=False, indent=4)
    f.close()

    timestamp4 = time.clock()
    print("Total write txt file Time is:", timestamp4 - timestamp3)

    with open(log_files_from_log, "rb") as fp_open:
        reopen_log_file = json.load(fp_open)
    fp_open.close()

    # write_log_to_file = open('log_files_from_log', 'w')
    # write_log_to_file.writelines(new_list_from_log)
    # write_log_to_file.close()

    timestamp5 = time.clock()
    print("Total load txt file Time is:", timestamp5 - timestamp4)

    # write_dict_to_csv_file
    # write_dict_to_csv_file(permit_dict_map, permit_csv_path)
    # write_dict_to_csv_file(deny_dict_map, deny_csv_path)
    # timestamp4 = time.clock()
    #
    # # timestamp4 - timestamp3 = write_dict_to_csv_file time
    # print("Total Write csv Time is:", timestamp4 - timestamp3)
    #
    # # write permit_csv to permit_excel
    # open_permit_csv_path = open(permit_csv_path, 'r')
    # all_permit_lines = open_permit_csv_path.readlines()
    # permit_excel = xlwt.Workbook(encoding='utf-8')
    # csv_split_to_sheet(QRC_subnet_list, all_permit_lines, permit_excel)
    # csv_split_to_sheet_for_others(QRC_subnet_list, all_permit_lines, permit_excel)
    # permit_excel.save(permit_rule_exl_path)
    # open_permit_csv_path.close()
    # # write deny_csv to deny_excel
    # open_deny_csv_path = open(deny_csv_path, 'r')
    # all_deny_lines = open_deny_csv_path.readlines()
    # deny_excel = xlwt.Workbook(encoding='utf-8')
    # csv_split_to_sheet(QRC_subnet_list, all_deny_lines, deny_excel)
    # csv_split_to_sheet_for_others(QRC_subnet_list, all_deny_lines, deny_excel)
    # deny_excel.save(deny_rule_exl_path)
    # open_deny_csv_path.close()
    # timestamp5 = time.clock()
    #
    # # timestamp5 - timestamp4 = write permit_excel time.
    # print("Total Write rule_file Time is:", timestamp5 - timestamp4)
    # print("Total Time used:", timestamp5 - timestamp1)
    #
