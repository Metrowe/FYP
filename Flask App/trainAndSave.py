 # TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import os

# Version of Tensorflow
print(tf.__version__)

# Get fashion dataset from library
fashion_mnist = keras.datasets.fashion_mnist
# Loads into a training set of 60,000 images and a test set of 10,000
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# Indexes are stored in the labels so this is needed to get the text labels
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Shows 60,000 images are there
print(train_images.shape)

# Shows 60,000 labels are there
print(len(train_labels))

# Shows 60,000 images are there
print(train_images.shape)

# Shows the indexes range from 0 - 9 
print(train_labels)

# The same can be repeated for the test images to show 10,000

# Pre-process images in same way to get them in the 0 - 1 range
train_images = train_images / 255.0
test_images = test_images / 255.0

# Added path for storing models
checkpoint_path = "training_model/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, 
                                                 save_weights_only=True,
                                                 verbose=1)


# Flattens arrays into a more easily processible design
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

# Compile the model some settings
model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Trains the model using all 60,000 training images
model.fit(train_images, train_labels, epochs=5,
			callbacks = [cp_callback])

# Evaluates the whole range of test data to evaluate success
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test accuracy:', test_acc)