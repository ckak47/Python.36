from __future__ import absolute_import, division, print_function
import tensorflow as tf
import pathlib
import random
import IPython.display as display


def preprocess_image(image):
  image = tf.image.decode_png(image, channels=3)
  image = tf.image.resize_images(image, [192, 192])
  # image /= 255.0  # normalize to [0,1] range
  return image


def load_and_preprocess_image(path):
  image = tf.read_file(path)
  return preprocess_image(image)


def load_and_preprocess_from_path_label(path, label):
  return load_and_preprocess_image(path), label


def change_range(image, label):
  return 2*image-1, label


tf.enable_eager_execution()

data_root = pathlib.Path("F:\\DeepTraffic-master\\1.malware_traffic_classification\\2.PreprocessedTools(USTC-TK2016)\\4_Png\\Train")
print(data_root)
# for item in data_root.iterdir():
#   print(item)


all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]
random.shuffle(all_image_paths)

image_count = len(all_image_paths)
print(image_count)


label_names = sorted(item.name for item in data_root.glob('*/') if item.is_dir())
print(label_names)


label_to_index = dict((name, index) for index, name in enumerate(label_names))
all_image_labels = [label_to_index[pathlib.Path(path).parent.name] for path in all_image_paths]
print("First 15 labels indices: ", all_image_labels[:14])


img_path = all_image_paths[0]
img_raw = tf.read_file(img_path)
print(repr(img_raw)[:100]+"...")
img_tensor = tf.image.decode_image(img_raw)

print(img_tensor.shape)
print(img_tensor.dtype)


img_final = img_tensor/255.0
print(img_final.shape)
print(img_final.numpy().min())
print(img_final.numpy().max())


path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)

# print('shape: ', repr(path_ds.output_shapes))
# print('type: ', path_ds.output_types)
# print()
# print(path_ds)

# image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=AUTOTUNE)
image_ds = path_ds.map(load_and_preprocess_image)
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))

for label in label_ds.take(10):
  print(label_names[label.numpy()])

image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

print('image shape: ', image_label_ds.output_shapes[0])
print('label shape: ', image_label_ds.output_shapes[1])
print('types: ', image_label_ds.output_types)
print()
print(image_label_ds)

ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))

image_label_ds = ds.map(load_and_preprocess_from_path_label)
print(image_label_ds)

BATCH_SIZE = 32

# Setting a shuffle buffer size as large as the dataset ensures that the data is
# completely shuffled.
ds = image_label_ds.shuffle(buffer_size=image_count)
ds = ds.repeat()
ds = ds.batch(BATCH_SIZE)
# `prefetch` lets the dataset fetch batches, in the background while the model is training.
ds = ds.prefetch(buffer_size=image_count)

ds = image_label_ds.apply(tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE)
ds = ds.prefetch(buffer_size=image_count)

mobile_net = tf.keras.applications.MobileNetV2(input_shape=(96, 96, 3), include_top=False)
mobile_net.trainable = False

keras_ds = ds.map(change_range)

image_batch, label_batch = next(iter(keras_ds))

feature_map_batch = mobile_net(image_batch)
print(feature_map_batch.shape)


model = tf.keras.Sequential([
  mobile_net,
  tf.keras.layers.GlobalAveragePooling2D(),
  tf.keras.layers.Dense(len(label_names))])

logit_batch = model(image_batch).numpy()

print("min logit:", logit_batch.min())
print("max logit:", logit_batch.max())
print()

print("Shape:", logit_batch.shape)

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=["accuracy"])

model.summary()

steps_per_epoch = tf.ceil(len(all_image_paths)/BATCH_SIZE).numpy()

model.fit(ds, epochs=1, steps_per_epoch=3)
print()




