import snap7
from snap7.util import *
import sys

plc = snap7.client.Client()

# plc.connect("PLC IP address",rack,slot)
plc.connect("192.168.1.1", 0, 2)

# plc.db_read(DATABASE,OFFSET,NUMBEROFBYTES)
# for INTEGER VALUE i read 2 BYTES
db = plc.db_read(123,12,2)

plc.disconnect()

for value in db:
        print("%03d" % value, sys.stdout.write(''))

print("")