# XuZhouDT.massage.check.list.PY.36.V.0.1.py write by python 3.6
import csv
import time
import os

# set the log file and dir
ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
log_file = "messages.1"
log_dir = "D:\\"
log_file_root_dir = "D:\\105_Train.log\\01.20160930.CQL6.Radio.Event\\Radio data"
log_csv_root_dir = "D:\\105_Train.log\\01.20160930.CQL6.Radio.Event\\"


def log_split_to_csv(log_line, new_list):
    #
    # This log_split_to_dict only for Checkpoint R80.10.
    #
    log_line_split = log_line.split(' ', 4)
    try:
        log_date = log_line_split[0] + " " + log_line_split[1]
    except IndexError:
        pass
    try:
        log_time = log_line_split[2]
    except IndexError:
        pass
    try:
        log_train_name = log_line_split[3]
    except IndexError:
        pass
    try:
        log_massage_all = log_line_split[4][0:-1]
    except IndexError:
        pass
    try:
        log_massage_split = log_massage_all.split(':', 3)
        try:
            log_massage_01 = log_massage_split[0]
        except IndexError:
            log_massage_01 = " "
        try:
            log_massage_02 = log_massage_split[1]
        except IndexError:
            log_massage_02 = " "
        try:
            log_massage_03 = log_massage_split[2]
        except IndexError:
            log_massage_03 = " "

        new_data_time = "2016" + " " + log_date + " " + log_time
        new_log = [new_data_time, log_train_name, log_massage_01, log_massage_02, log_massage_03]
        new_list.append(new_log)

    except UnboundLocalError:
        pass


if __name__ == '__main__':
    # set time variable used in file_names
    timestamp1 = time.clock()

    log_path_list = os.listdir(log_file_root_dir)
    all_train_list_from_log = []

    # This module open the root_log_dir log_files.
    for index_01 in range(0, len(log_path_list)):
        time_begin = time.clock()
        log_file_path01 = os.path.join(log_file_root_dir, log_path_list[index_01])
        log_file_list = os.listdir(log_file_path01)
        train_name = log_path_list[index_01]
        each_train_list_from_log = []
        print("Process with the %s log file ." % train_name)
        for index_02 in range(0, len(log_file_list)):
            log_file_path02 = os.path.join(log_file_path01, log_file_list[index_02])
            open_log_file = open(log_file_path02, 'r')
            try:
                all_log_lines = open_log_file.readlines()
                open_log_file.close()
                for each_log_line in all_log_lines:
                    log_split_to_csv(each_log_line, each_train_list_from_log)
            except UnicodeDecodeError:
                pass
        log_file_write_to_csv_path = log_csv_root_dir + train_name + "." + ticks + ".csv"
        with open(log_file_write_to_csv_path, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(each_train_list_from_log)
        time_end = time.clock()
        print("Time for process %s log file is %s" % (train_name, time_end - time_begin))

    timestamp2 = time.clock()
    print("Total time for process Log file used:", timestamp2 - timestamp1)

    timestamp3 = time.clock()
    print("Total Split Log file Time used:", timestamp3 - timestamp2)

    timestamp4 = time.clock()
    print("Total write Log file to csv Time used:", timestamp4 - timestamp3)

