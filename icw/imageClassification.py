from tensorflow import keras
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

# import errorHandling as error
import modelConfiguration 

# The label strings are path to the weights file are stored as global variables 
# class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
# checkpoint_path = "training_model/cp.ckpt"

# def createModel():
# 	# Model is structured as a sequence of 1D Arrays
# 	newModel = keras.Sequential([
# 	    keras.layers.Flatten(input_shape=(28, 28)),
# 	    keras.layers.Dense(128, activation=tf.nn.relu),
# 	    keras.layers.Dense(10, activation=tf.nn.softmax)
# 	])

# 	# Compile the model with settings
# 	newModel.compile(optimizer=tf.train.AdamOptimizer(), 
# 	              loss='sparse_categorical_crossentropy',
# 	              metrics=['accuracy'])

# 	return newModel

theModel = None

def getWeightedModel():
	checkpoint_path = "training_model/cp.ckpt"
	newModel = modelConfiguration.createModel()

	newModel.load_weights(modelConfiguration.checkpoint_path)
	return newModel	

# def formatImage(image):
# 	# Convert from openCVs default BGR to grayscale
# 	tempImage = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
	
# 	# Resize image to same as input samples
# 	tempImage = cv2.resize(tempImage, (28, 28))

# 	# Invert image
# 	tempImage = cv2.bitwise_not(tempImage)

# 	# Get values in range 0 - 1
# 	tempImage = tempImage / 255.0

# 	return tempImage


# def classifyImage(imagePath,model):
def classifyImage(imagePath,destpath):
	global theModel
	if theModel == None:
		theModel = getWeightedModel()

	# theModel = getWeightedModel()
	# Gets the image from the path and formats it to be the same as the training data
	original = cv2.imread(imagePath)
	finalImage = modelConfiguration.formatImage(original)

	cv2.imwrite(destpath,finalImage)

	# Generates the predictions for the specified image
	prediction = theModel.predict(np.array( [finalImage,] ) )
	# Finds the highest probability prediction and returns the corresponding label
	result = modelConfiguration.class_names[np.argmax(prediction[0])]

	return result

