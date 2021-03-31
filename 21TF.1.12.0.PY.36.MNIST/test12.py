'''Trains a simple deep NN on the MNIST dataset.

Gets to 83.57% test accuracy after 30 epochs
(there is *a lot* of margin for parameter tuning).
33 seconds on a GTX1080 GPU.
179 seconds on a P2000(mobile) GPU.
'''
from __future__ import print_function

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import time
import numpy

img_rows, img_cols = 28, 28
batch_size = 128
num_classes = 14
epochs = 30

# the data, split between train and test sets
Timestamp1 = time.clock()
print("Begin load Data. ")

x_train = numpy.load('F:\\104_Traffic\\x_train.npy')
y_train = numpy.load('F:\\104_Traffic\\y_train.npy')
x_test = numpy.load('F:\\104_Traffic\\x_test.npy')
y_test = numpy.load('F:\\104_Traffic\\y_test.npy')

Timestamp2 = time.clock()
print("Finish load Data. Total Time use: ", Timestamp2 - Timestamp1)

x_train = x_train.reshape(56808, 784)
x_test = x_test.reshape(6312, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

print("Begin train the model. ")

Timestamp3 = time.clock()

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=0,
                    validation_data=(x_test, y_test))

Timestamp4 = time.clock()
print("End train the model, Total train time use seconds of: ", Timestamp4 - Timestamp3)

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
