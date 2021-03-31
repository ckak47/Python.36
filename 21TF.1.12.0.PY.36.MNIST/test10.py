'''
Convert images from diff dict to ndarray.
And save the ndarray to a local files.
'''
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import pathlib
import random
import numpy
from PIL import Image
from tempfile import TemporaryFile
import binascii
import errno
import os
import IPython.display as display
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import time

batch_size = 128
num_classes = 14
epochs = 12
img_rows, img_cols = 28, 28
data_root_test = pathlib.Path("F:\\104_Traffic\\TrimedSession\\Test")
data_root_train = pathlib.Path("F:\\104_Traffic\\TrimedSession\\Train")
print(data_root_test)
print(data_root_train)


def convert_bin_2_ndarray(img_path, width):
    with open(img_path, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i+2], 16) for i in range(0, len(hexst), 2)])
    rn = int(len(fh)/width)
    fh = numpy.reshape(fh[:rn*width], (-1, width))
    fh = numpy.uint8(fh)
    return fh


for item in data_root_test.iterdir():
    print(item)

for item in data_root_train.iterdir():
    print(item)

all_image_paths_test = list(data_root_test.glob('*/*'))
all_image_paths_test = [str(path) for path in all_image_paths_test]
random.shuffle(all_image_paths_test)

all_image_paths_train = list(data_root_train.glob('*/*'))
all_image_paths_train = [str(path) for path in all_image_paths_train]
random.shuffle(all_image_paths_train)

image_count_test = len(all_image_paths_test)
print(image_count_test)
print(all_image_paths_test[:10])

image_count_train = len(all_image_paths_train)
print(image_count_train)
print(all_image_paths_train[:10])


label_names_test = sorted(item.name for item in data_root_test.glob('*/') if item.is_dir())
print(label_names_test)

label_names_train = sorted(item.name for item in data_root_train.glob('*/') if item.is_dir())
print(label_names_train)

label_to_index_test = dict((name, index) for index, name in enumerate(label_names_test))
print(label_to_index_test)

label_to_index_train = dict((name, index) for index, name in enumerate(label_names_train))
print(label_to_index_train)


all_image_labels_test = [label_to_index_test[pathlib.Path(path).parent.name]
                         for path in all_image_paths_test]

print("First Test 20 labels indices: ", all_image_labels_test[:20])

all_image_labels_train = [label_to_index_train[pathlib.Path(path).parent.name]
                          for path in all_image_paths_train]

print("First Train 20 labels indices: ", all_image_labels_train[:20])

img_path_test = all_image_paths_test[0]
print(img_path_test)

img_path_train = all_image_paths_train[0]
print(img_path_train)

Timestamp1 = time.clock()
print("Begin load test image. ")
i = 1
for p in all_image_paths_test:
    if i == 1:
        x_test_1 = convert_bin_2_ndarray(p, img_rows)
        x_test = numpy.expand_dims(x_test_1, axis=0)
        i = i+1
    else:
        x_test = numpy.append(x_test, [convert_bin_2_ndarray(p, img_rows)], axis=0)
Timestamp2 = time.clock()
print("Finish load test image, Ues time of second: ", Timestamp2-Timestamp1)

print("Begin load train image. ")
j = 1
for q in all_image_paths_train:
    if j == 1:
        x_train_1 = convert_bin_2_ndarray(q, img_rows)
        x_train = numpy.expand_dims(x_train_1, axis=0)
        j = j+1
    else:
        x_train = numpy.append(x_train, [convert_bin_2_ndarray(q, img_rows)], axis=0)
Timestamp3 = time.clock()
print("Finish load train image, Ues time of second: ", Timestamp3-Timestamp2)

y_test = numpy.asarray(all_image_labels_test, dtype=numpy.uint8)
y_train = numpy.asarray(all_image_labels_train, dtype=numpy.uint8)

numpy.save('F:\\104_Traffic\\x_train.npy', x_train)
numpy.save('F:\\104_Traffic\\y_train.npy', y_train)
numpy.save('F:\\104_Traffic\\x_test.npy', x_test)
numpy.save('F:\\104_Traffic\\y_test.npy', y_test)
