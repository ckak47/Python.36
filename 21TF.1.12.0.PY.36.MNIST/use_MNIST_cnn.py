from __future__ import absolute_import, division, print_function
import tensorflow as tf
import pathlib
import random
import numpy as np
import keras
from keras import applications
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K


data_root_train = pathlib.Path("F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\4_Png\\Train")
data_root_test = pathlib.Path("F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\4_Png\\Test")

batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
img_rows, img_cols = 28, 28


def preprocess_image(image):
  image = tf.image.decode_png(image, channels=3)
  image = tf.image.resize_images(image, [28, 28])
  image /= 255.0  # normalize to [0,1] range
  return image


def load_and_preprocess_image(path):
  image = tf.read_file(path)
  return preprocess_image(image)


def load_and_preprocess_from_path_label(path, label):
  return load_and_preprocess_image(path), label


def change_range(image, label):
  return 2*image-1, label


# data_root = pathlib.Path("F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\4_Png\\Train")
print()
print("the data_root_train dict path is : ", data_root_train)
print()
print("the data_root_test dict path is : ", data_root_test)

# glob the hole dict
all_image_paths_train = list(data_root_train.glob('*/*'))
all_image_paths_test = list(data_root_test.glob('*/*'))
all_image_paths_train = [str(path) for path in all_image_paths_train]
all_image_paths_test = [str(path) for path in all_image_paths_test]

# random the img path
random.shuffle(all_image_paths_train)
random.shuffle(all_image_paths_test)

# count the image
image_count_train = len(all_image_paths_train)
image_count_test = len(all_image_paths_test)
print()
print("the total number of img is : ", image_count_train)
print()
print("the total number of img is : ", image_count_test)
print()

# get the labels for the image
label_names_train = sorted(item.name for item in data_root_train.glob('*/') if item.is_dir())
label_names_test = sorted(item.name for item in data_root_test.glob('*/') if item.is_dir())
print()
print("the total label of the train img are : ", label_names_train)
print()
print("the total label of the test img are : ", label_names_test)
print()

# index the labels
label_to_index_train = dict((name, index) for index, name in enumerate(label_names_train))
label_to_index_test = dict((name, index) for index, name in enumerate(label_names_test))
all_image_labels_train = [label_to_index_train[pathlib.Path(path).parent.name] for path in all_image_paths_train]
all_image_labels_test = [label_to_index_test[pathlib.Path(path).parent.name] for path in all_image_paths_test]

path_ds_train = tf.data.Dataset.from_tensor_slices(all_image_paths_train)
path_ds_test = tf.data.Dataset.from_tensor_slices(all_image_paths_test)
image_ds_train = path_ds_train.map(load_and_preprocess_image)
image_ds_test = path_ds_test.map(load_and_preprocess_image)
label_ds_train = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels_train, tf.int64))
label_ds_test = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels_test, tf.int64))

# Combine the image and labels
image_label_ds_train = tf.data.Dataset.zip((image_ds_train, label_ds_train))
image_label_ds_test = tf.data.Dataset.zip((image_ds_test, label_ds_test))
print()
ds_train = tf.data.Dataset.from_tensor_slices((all_image_paths_train, all_image_labels_train))
ds_test = tf.data.Dataset.from_tensor_slices((all_image_paths_test, all_image_labels_test))
print()
image_label_ds_train = ds_train.map(load_and_preprocess_from_path_label)
image_label_ds_test = ds_test.map(load_and_preprocess_from_path_label)
print()


iterator = tf.data.Iterator.from_structure(image_label_ds_train.output_types,
                                           image_label_ds_train.output_shapes)
next_element = iterator.get_next()

training_init_op = iterator.make_initializer(image_label_ds_train)
validation_init_op = iterator.make_initializer(image_label_ds_test)

print()

mobile_net = tf.keras.applications.MobileNetV2(input_shape=(192, 192, 3), include_top=False)
mobile_net.trainable = False

keras_ds_train = ds_train.map(change_range)
keras_ds_test = ds_test.map(change_range)

image_batch, label_batch = next(iter(keras_ds_train))

feature_map_batch = mobile_net(image_batch)
print(feature_map_batch.shape)
print()



# for _ in range(20):
#   with tf.Session() as sess:
#     # Initialize an iterator over the training dataset.
#     sess.run(training_init_op)
#     for _ in range(100):
#       sess.run(next_element)
#
#     # Initialize an iterator over the validation dataset.
#     sess.run(validation_init_op)
#     for _ in range(50):
#       sess.run(next_element)

# with tf.Session() as sess:
#
#   # initialize the iterator on the training data
#   sess.run(training_init_op)
#
#   # get each element of the training dataset until the end is reached
#   while True:
#     try:
#       elem = sess.run(next_element)
#       # print(elem)
#     except tf.errors.OutOfRangeError:
#       print("End of training dataset.")
#       break
#
#   # initialize the iterator on the validation data
#   sess.run(validation_init_op)
#
#   # get each element of the validation dataset until the end is reached
#   while True:
#     try:
#       elem = sess.run(next_element)
#       print(elem)
#     except tf.errors.OutOfRangeError:
#       print("End of training dataset.")
#       break
# print()
