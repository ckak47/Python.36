# cdc_dns_check write by python 3.6
import csv
import IPy
import time
import xlwt
import os
import tldextract

# start time stamp
timestamp1 = time.clock()
log_file = "auth.log"
log_dir = "E:\\LOG.SSH\\"


def invalid_log_split_to_dict(log_line, dict_map):
    #
    # This invalid_log_split_to_dict only for invalid login in SSH Log.
    #
    log_line_split = log_line.split(' ')
    month_from_log = log_line_split[0]
    day_from_log = log_line_split[1]
    time_from_log = log_line_split[2]
    invalid_user_name_from_log = log_line_split[7]
    ip_addr_from_log = log_line_split[9][0:-2]
    data_and_time = month_from_log + " " + day_from_log + " " + time_from_log
    new_log = (invalid_user_name_from_log, ip_addr_from_log)
    if new_log not in dict_map.keys():
        set_data_and_time_val = {
            "start": data_and_time,
            "end": data_and_time,
        }
        dict_map[new_log] = set_data_and_time_val
    else:
        dict_map[new_log]["end"] = data_and_time


def failed_root_log_split_to_dict(log_line, dict_map):
    #
    # This failed_root_log_split_to_dict only for failed login in SSH Log.
    #
    log_line_split = log_line.split(' ')
    month_from_log = log_line_split[0]
    day_from_log = log_line_split[1]
    time_from_log = log_line_split[2]
    invalid_user_name_from_log = log_line_split[8]
    ip_addr_from_log = log_line_split[10]
    data_and_time = month_from_log + " " + day_from_log + " " + time_from_log
    new_log = (invalid_user_name_from_log, ip_addr_from_log)
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
        # csv_lenth = 0
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['invalid_user_name', 'ip_addr', 'first_time', 'last_time'])
        for k, v in dict_map.items():
            log_lists = []
            for _ in k:
                log_lists.append(_)
            for j in v.values():
                log_lists.append(j)
            try:
                # IPy.IP(log_lists[2]) and IPy.IP(log_lists[3])
                csv_writer.writerow(log_lists)
                # csv_lenth += 1
            except Exception as e:
                pass


if __name__ == '__main__':
    # set time variable used in file_names
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    log_file_list = os.listdir(log_dir)

    invalid_dict_map = {}
    failed_root_dict_map = {}

    invalid_csv_path = log_dir + "invalid" + "." + ticks + ".csv"
    failed_root_csv_path = log_dir + "failed_root" + "." + ticks + ".csv"

    for index in range(0, len(log_file_list)):
        log_path = os.path.join(log_dir, log_file_list[index])
        open_log_file = open(log_path, 'r')
        all_log_lines = open_log_file.readlines()
        open_log_file.close()
        for each_log_line in all_log_lines:
            if "Invalid" in each_log_line:
                invalid_log_split_to_dict(each_log_line, invalid_dict_map)
            elif "Failed password for root" in each_log_line:
                if "message repeated" not in each_log_line:
                    failed_root_log_split_to_dict(each_log_line, failed_root_dict_map)

    timestamp3 = time.clock()
    print(len(invalid_dict_map))
    print(len(failed_root_dict_map))
    write_dict_to_csv_file(invalid_dict_map, invalid_csv_path)
    write_dict_to_csv_file(failed_root_dict_map, failed_root_csv_path)
    timestamp4 = time.clock()
    # timestamp4 - timestamp3 = write_dict_to_csv_file time
    print("Total Write csv Time is:", timestamp4 - timestamp3)
