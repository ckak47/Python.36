# QRC.Firewall.check.list.PY.36.V.3.0.py write by python 3.6
import csv
import time

timestamp1 = time.clock()

# set the log filename and dir
log_filename = "QD.QRC.CP5600.R77.30.20181015.log"
log_dir = "D:\\"

# set time variable in filename
ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())

file_path = log_dir + log_filename
permit_CSV_path = log_dir + log_filename + "." + "permit" + "." + ticks + ".csv"
deny_CSV_path = log_dir + log_filename + "." + "deny" + "." + ticks + ".csv"

if __name__ == '__main__':
    # open log file
    all_permit_logs = set()
    all_deny_logs = set()
    open_log_file = open(file_path, 'r')
    for each_log_line in open_log_file:
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
                _tuple = (Interface, Action, Source, Destination, Service, Protocal)
                all_permit_logs.add(_tuple)
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
                _tuple = (Interface, Action, Source, Destination, Service, Protocal)
                all_deny_logs.add(_tuple)
    open_log_file.close()
    timestamp2 = time.clock()

    # write the set to csv files
    all_permit_logs_list = list(all_permit_logs)
    all_deny_logs_list = list(all_deny_logs)
    with open(permit_CSV_path, 'w', newline='') as permite_CSV_file:
        permite_writer = csv.writer(permite_CSV_file)
        permite_writer.writerow(['Interface', 'Action', 'Source', 'Destination', 'Service', 'Protocal', 'Date'])
        for permite_rows in all_permit_logs_list:
            permite_writer.writerow(permite_rows)
    with open(deny_CSV_path, 'w', newline='') as deny_CSV_file:
        deny_writer = csv.writer(deny_CSV_file)
        deny_writer.writerow(['Interface', 'Action', 'Source', 'Destination', 'Service', 'Protocal', 'Date'])
        for deny_rows in all_deny_logs_list:
            deny_writer.writerow(deny_rows)
    timestamp3 = time.clock()

    print("Total Read Log file Time used:", timestamp2 - timestamp1)
    print("Total Write csv Time is:", timestamp3 - timestamp2)
    print("Total Time used:", timestamp3 - timestamp1)

