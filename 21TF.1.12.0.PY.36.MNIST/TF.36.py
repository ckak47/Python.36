import tensorflow as tf
from numpy.random import RandomState

batch_size = 8

w1 = tf.Variable(tf.random_normal((2, 3), stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal((3, 1), stddev=1, seed=1))
#x = tf.placeholder(tf.float32, shape=(1, 2), name="input")

x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

a = tf.nn.relu(tf.matmul(x, w1), name=None)
y = tf.nn.relu(tf.matmul(a, w2), name=None)

y = tf.sigmoid(y)
cross_entropy = -tf.reduce_mean(
    y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
    +(1-y) * tf.log(tf.clip_by_value(1-y, 1e-10, 1.0))
)
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

rdm = RandomState(1)
dataset_size = 128

X = rdm.rand(dataset_size, 2)
Y = [[int(x1+x2 < 1)] for (x1, x2) in X]

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    print(sess.run(w1))
    print(sess.run(w2))

    STEPS = 5000
    for i in range(STEPS):
        start = (i * batch_size) % dataset_size
        end = min(start+batch_size, dataset_size)
        sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})
        if i % 1000 == 0:
            total_cross_entropy = sess.run(cross_entropy, feed_dict={x: X, y_: Y})
            print(i, total_cross_entropy)
    print(sess.run(w1))
    print(sess.run(w2))

import tensorflow as tf
tf.keras.backend.clear_session()









































import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
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

model = Sequential()
model.add(
    Conv2D(32, kernel_size=(5, 5), activation='relu', input_shape=input_shape)
)
model.add(
    MaxPooling2D(pool_size=(2, 2))
)
model.add(
    Conv2D(64, kernel_size=(5, 5), activation='relu')
)
model.add(
    MaxPooling2D(pool_size=(2, 2))
)
model.add(
    Flatten()
)
model.add(
    Dense(500, activation='relu')
)
model.add(
    Dense(num_classes, activation='softmax')
)

model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.SGD(),
    metrics=['accuracy']
)

model.fit(
    trainX,
    trainY,
    batch_size=128,
    epochs=20,
    validation_data=(testX,testY)
)
score = model.evaluate(testX, testY)
print('test loss:', score[0])
print('test accuracy', score[1])















