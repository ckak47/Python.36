import numpy
from PIL import Image
import binascii
import errno
import os

PNG_SIZE = 28


def getMatrixfrom_pcap(filename, width):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i+2], 16) for i in range(0, len(hexst), 2)])
    rn = int(len(fh)/width)
    fh = numpy.reshape(fh[:rn*width], (-1, width))
    fh = numpy.uint8(fh)
    return fh


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


path_for_train = "F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\3_ProcessedSession\\TrimedSession\\Train"
path_for_test = "F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\3_ProcessedSession\\TrimedSession\\Test"
path_for_jpg_train = "F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\4_Png\\Train_192"
path_for_jpg_test = "F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\4_Png\\Test_192"
paths = [[path_for_train, path_for_jpg_train], [path_for_test, path_for_jpg_test]]
for p in paths:
    for i, d in enumerate(os.listdir(p[0])):
        dir_full = os.path.join(p[1], str(i))
        mkdir_p(dir_full)
        for f in os.listdir(os.path.join(p[0], d)):
            bin_full = os.path.join(p[0], d, f)
            im = Image.fromarray(getMatrixfrom_pcap(bin_full, PNG_SIZE))
            png_full = os.path.join(dir_full, os.path.splitext(f)[0]+'.png')
            im.save(png_full)