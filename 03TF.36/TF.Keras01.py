import keras
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense, Input
from keras import backend as K

num_classes = 10
img_rows, img_cols = 28, 28

(trainX, trainY), (testX, testY) = mnist.load_data('E:\mnist\mnist.npz')

if K.image_data_format() == 'channels_first':
    trainX = trainX.reshape(trainX.shape[0], 1, img_rows, img_cols)
    testX = testX.reshape(testX.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    trainX = trainX.reshape(trainX.shape[0], img_rows, img_cols, 1)
    testX = testX.reshape(testX.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

trainX = trainX.astype('float32')
testX = testX.astype('float32')
trainX /= 255.0
testX /= 255.0

trainY = keras.utils.to_categorical(trainY, num_classes)
testY = keras.utils.to_categorical(testY, num_classes)

#inputs = Input(shape=(60000, 28, 28))

input1 = Input(shape=(784,), name="input1")
input2 = Input(shape=(10,), name="input2")

x = Dense(1, activation='relu')(input1)

output1 = Dense(10, activation='softmax', name="output1")(x)

y = keras.layers.concatenate([x, input2])

output2 = Dense(10, activation='softmax', name="output2")(y)

model = Model(inputs=[input1, input2], outputs=[output1, output2])

model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.SGD(),
    loss_weights=[1, 0.1],
    metrics=['accuracy']
)

model.fit(
    {'input1': trainX, 'input2': trainY},
    {'output1': trainY, 'output2': trainY},
    batch_size=128,
    epochs=20,
    validation_data=([testX, testY], [testY, testY])
)
score = model.evaluate(testX, testY)
print('test loss:', score[0])
print('test accuracy', score[1])
