# QRC.Firewall.check.list.PY.36.V.3.0.py write by python 3.6
import csv
import IPy
import time
import xlwt

# start time stamp
timestamp1 = time.clock()

# set the log file and dir
log_file = "SH.BG.CP5600.R80.10.20190619.log.permit.20190624155153.csv"
log_dir = "D:\\"

wired_ip_list = ["152.3.4.3",
                 "152.3.5.3",
                 "152.3.8.107",
                 "152.3.8.150",
                 "152.3.8.213",
                 "152.3.8.210"]

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

    for each_wired_ip_list in wired_ip_list:
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
            print("Total ", each_wired_ip_csv_path, "file len :", csv_lenth)

    timestamp3 = time.clock()
