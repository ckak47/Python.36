'''Trains a simple convnet on the MNIST dataset.
Use the data from test10.py
Gets to 86.37% test accuracy after 20 epochs
(there is still a lot of margin for parameter tuning).
90 seconds on a GTX 1080 GPU.
1630 seconds on a P2000 GPU.
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
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import time

batch_size = 128
num_classes = 14
epochs = 20
img_rows, img_cols = 28, 28

Timestamp1 = time.clock()
print("Begin load Data. ")

x_train = numpy.load('F:\\104_Traffic\\x_train.npy')
y_train = numpy.load('F:\\104_Traffic\\y_train.npy')
x_test = numpy.load('F:\\104_Traffic\\x_test.npy')
y_test = numpy.load('F:\\104_Traffic\\y_test.npy')

Timestamp2 = time.clock()
print("Finish load Data. Total Time use: ", Timestamp2 - Timestamp1)

print("Begin train the model. ")
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

Timestamp3 = time.clock()

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=0,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
Timestamp4 = time.clock()
print("End train the model, Total train time use seconds of: ", Timestamp4 - Timestamp3)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
