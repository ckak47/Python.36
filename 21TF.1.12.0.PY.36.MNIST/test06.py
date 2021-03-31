from __future__ import absolute_import, division, print_function

import tensorflow as tf
import pathlib
import random
import IPython.display as display


data_root = pathlib.Path("D:\\104_Traffic\\FilteredSession\\Test")
print(data_root)

for item in data_root.iterdir():
    print(item)

all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]
random.shuffle(all_image_paths)

image_count = len(all_image_paths)
print(image_count)
print(all_image_paths[:10])


def caption_image(image_path):
    image_rel = pathlib.Path(image_path).relative_to(data_root)
    return "Image (CC BY 2.0) "


# for n in range(3):
#   image_path = random.choice(all_image_paths)
#   display.display(display.Image(image_path))
#   print(caption_image(image_path))
#   print()

label_names = sorted(item.name for item in data_root.glob('*/') if item.is_dir())
print(label_names)

label_to_index = dict((name, index) for index, name in enumerate(label_names))
print(label_to_index)

all_image_labels = [label_to_index[pathlib.Path(path).parent.name]
                    for path in all_image_paths]

print("First 10 labels indices: ", all_image_labels[:10])

img_path = all_image_paths[0]
print(img_path)

img_raw = tf.read_file(img_path)
print(repr(img_raw)[:100]+"...")

# img_tensor = tf.image.decode_image(img_raw)
img_tensor = tf.image.decode_png(img_raw)

print(img_tensor.shape)
print(img_tensor.dtype)



print()