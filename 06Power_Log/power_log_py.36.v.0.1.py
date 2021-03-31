from scapy.all import *
from elasticsearch import Elasticsearch
from datetime import datetime
import binascii


log_file_location = ("D:\\power.2020.01.03.cap")

all_pcap_files = rdpcap(log_file_location)

for cap_packet in all_pcap_files:
    cap_timestamp = cap_packet.time
    cap_src_ip = cap_packet.payload.src
    cap_dst_ip = cap_packet.payload.dst
    cap_src_tcp_port = cap_packet.payload.payload.sport
    cap_dst_tcp_port = cap_packet.payload.payload.dport
    cap_tcp_payload = str(binascii.b2a_hex(cap_packet.payload.payload.payload.original))
    mark_01 = cap_tcp_payload[2:4]
    mark_02 = cap_tcp_payload[12:14]
    if mark_01 == str(68) and mark_02 == str(68):
        cap_control_bit = cap_tcp_payload[14:16]
        cap_A1_up = cap_tcp_payload[18:20]
        cap_A1_down = cap_tcp_payload[16:18]
        cap_A2 = cap_tcp_payload[20:24]
        cap_A3 = cap_tcp_payload[24:26]

        print("The IP", cap_src_ip, "'s control_bit is: ", cap_control_bit,
              "A1 code is: ", cap_A1_up + cap_A1_down, "A2 code is: ",
              cap_A2, "A3 code is: ", cap_A3)
