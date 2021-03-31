import time
import ipaddress
import xlwt
import IPy

if __name__ == '__main__':
    start = time.clock()
    Rule = "D:\QD.QRC.CP5600.R77.30.20181015.log.permit.20190304160054.csv"  # CSV文件位置
    new_csv = "D:\QD.QRC.CP5600.R77.30.20181015.log.permit.20190304160054.new.csv"  # 新的策略表位置
    fp = open(Rule, 'r')
    Alllines = fp.readlines()
    fp.close()
    new_csv_file = open(new_csv, 'w')
    all_new_lines = new_csv_file.readlines()
    for all_lines in Alllines:
        try:
            ipaddress.ip_address(all_lines[2]) and ipaddress.ip_address(all_lines[3])
            all_new_lines.append(all_lines)






