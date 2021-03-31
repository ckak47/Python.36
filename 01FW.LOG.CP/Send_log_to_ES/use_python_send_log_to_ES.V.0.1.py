#!/usr/bin/env python
"""
Written by Kang.Chen
Send Log file to ES.
"""
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time
import os
import IPy


log_dir = "D:\\Log.FW.DLP.CP5100"
customer_name = "dlp"
firewall_os_type = "fw_r80_10"


server_ip = ["139.24.22.234",
             "139.24.22.235",
             "139.24.22.236",
             "139.24.22.237",
             "139.24.22.238",
             "139.24.22.239",
             "139.24.22.240"]


def load_file_to_es(es_connect, input_files):
    for file in input_files:
        ACTIONS = []
        # 判断是否是文件夹，不是文件夹才打开
        if not os.path.isdir(file):
            # 打开文件
            open_log_file = open(log_dir + "\\" + file)
            all_log_lines = open_log_file.readlines()
            for each_log_line in all_log_lines:
                log_line_split = each_log_line.split(';')

                try:
                    IPy.IP(log_line_split[22], make_net=True) and IPy.IP(log_line_split[23], make_net=True)
                    set_of_log = {
                        'data_from_log': log_line_split[1],
                        'time_from_log': log_line_split[2],
                        'orig_device_ip': log_line_split[3],
                        'type_of_log': log_line_split[4],
                        'action_from_log': log_line_split[5],
                        'if_name': log_line_split[7],
                        'if_direction': log_line_split[8],
                        'product_type': log_line_split[9],
                        'service_id': log_line_split[18],
                        'src_ip': log_line_split[22],
                        'dst_ip': log_line_split[23],
                        'proto_tcp_or_udp': log_line_split[24],
                        'dst_port': log_line_split[34],
                        'src_port': log_line_split[35],
                    }
                    index_name = str.lower(customer_name + "_" + firewall_os_type + "_" + log_line_split[1])
                    ACTIONS.append(set_of_log)
                except Exception as e:
                    try:
                        IPy.IP(log_line_split[19], make_net=True) and IPy.IP(log_line_split[20], make_net=True)
                        set_of_log = {
                            'data_from_log': log_line_split[1],
                            'time_from_log': log_line_split[2],
                            'orig_device_ip': log_line_split[3],
                            'type_of_log': log_line_split[4],
                            'action_from_log': log_line_split[5],
                            'if_name': log_line_split[7],
                            'if_direction': log_line_split[8],
                            'product_type': log_line_split[9],
                            'service_id': log_line_split[18],
                            'src_ip': log_line_split[19],
                            'dst_ip': log_line_split[20],
                            'proto_tcp_or_udp': log_line_split[21],
                            'dst_port': log_line_split[29],
                            'src_port': log_line_split[30],
                        }
                        index_name = str.lower(customer_name + "_" + firewall_os_type + "_" + log_line_split[1])
                        ACTIONS.append(set_of_log)
                    except Exception as e:
                        try:
                            IPy.IP(log_line_split[21], make_net=True) and IPy.IP(log_line_split[22], make_net=True)
                            set_of_log = {
                                'data_from_log': log_line_split[1],
                                'time_from_log': log_line_split[2],
                                'orig_device_ip': log_line_split[3],
                                'type_of_log': log_line_split[4],
                                'action_from_log': log_line_split[5],
                                'if_name': log_line_split[7],
                                'if_direction': log_line_split[8],
                                'product_type': log_line_split[9],
                                'service_id': log_line_split[20],
                                'src_ip': log_line_split[21],
                                'dst_ip': log_line_split[22],
                                'proto_tcp_or_udp': log_line_split[23],
                                'dst_port': log_line_split[31],
                                'src_port': log_line_split[32],
                            }
                            index_name = str.lower(customer_name + "_" + firewall_os_type + "_" + log_line_split[1])
                            ACTIONS.append(set_of_log)
                        except Exception as e:
                            pass
            success, _ = bulk(es_connect, ACTIONS, index=index_name)
            es_connect.indices.refresh(index=index_name)
            print("load file:", file, "successfully.", "Total length is:", len(ACTIONS), ".")


if __name__ == '__main__':
    # start time stamp
    print("Starting file analysis . . .")
    timestamp1 = time.clock()
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())

    # try to connect the es instance.
    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        print("Connected", es.info())
    except Exception as ex:
        print("Error:", ex)
    # This module open the log_file.
    # 得到文件夹下的所有文件名称
    files = os.listdir(log_dir)

    load_file_to_es(es, files)
