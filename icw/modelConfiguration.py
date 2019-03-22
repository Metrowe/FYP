import tensorflow as tf
from tensorflow import keras

import cv2

checkpoint_path = "training_model/cp.ckpt"
class_names = ['antelope','bat','beaver','blue+whale','bobcat','buffalo','chihuahua','chimpanzee','collie','cow','dalmatian','deer','dolphin','elephant','fox','german+shepherd','giant+panda','giraffe','gorilla','grizzly+bear','hamster','hippopotamus','horse','humpback+whale','killer+whale','leopard','lion','mole','moose','mouse','otter','ox','persian+cat','pig','polar+bear','rabbit','raccoon','rat','rhinoceros','seal','sheep','siamese+cat','skunk','spider+monkey','squirrel','tiger','walrus','weasel','wolf','zebra']

def createModel():
	model = keras.models.Sequential()
	model.add(keras.layers.Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(200, 200, 3)))
	# model.add(keras.layers.Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(100, 100, 3)))
	# model.add(keras.layers.Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(50, 50, 3)))
	# model.add(keras.layers.Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(32, 32, 3)))
	model.add(keras.layers.MaxPooling2D(pool_size=2))
	model.add(keras.layers.Conv2D(filters=32,kernel_size=2,padding="same",activation="relu"))
	model.add(keras.layers.MaxPooling2D(pool_size=2))
	model.add(keras.layers.Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))
	model.add(keras.layers.MaxPooling2D(pool_size=2))
	model.add(keras.layers.Dropout(0.2))
	model.add(keras.layers.Flatten())
	model.add(keras.layers.Dense(500,activation="relu"))
	model.add(keras.layers.Dropout(0.2))
	# model.add(keras.layers.Dense(4,activation="softmax"))

	# First argument is number of output classes
	# model.add(keras.layers.Dense(10,activation="softmax"))
	model.add(keras.layers.Dense(50,activation="softmax"))

	# Compile the model with settings
	model.compile(optimizer=tf.train.AdamOptimizer(), 
	              loss='sparse_categorical_crossentropy',
	              metrics=['accuracy'])

	return model
	#add 32 then 16
	#go to 64 96 64 output

def makeSquare(image,padColour):
	height, width, channels = image.shape

	pad = int( ( abs(height - width) ) / 2 )

	if height > width:
		# cv2.ccopyMakeBorder(image,top,bottom,left,right)
		image = cv2.copyMakeBorder(image,0,0,pad,pad,cv2.BORDER_CONSTANT,value=padColour)
	elif width > height:
		image = cv2.copyMakeBorder(image,pad,pad,0,0,cv2.BORDER_CONSTANT,value=padColour)

	return image

# def formatImage(image,padColour,finalSize):
def formatImage(image):
	finalSize = 200
	padColour = [0,0,0]


	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	padded = makeSquare(image,padColour)
	resized = cv2.resize(padded,(finalSize,finalSize))

	normalised = resized / 255.0

	return resized

# def formatImage(image):
# 	# Convert from openCVs default BGR to RGB
# 	# tempImage = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
# 	tempImage = image.copy()
	
# 	# Resize image to same as input samples
# 	tempImage = cv2.resize(tempImage, (32, 32))

# 	# Get in range of zero to one so 
# 	tempImage = tempImage / 255.0

# 	# print(tempImage)

# 	# Invert image
# 	# tempImage = cv2.bitwise_not(tempImage)

# 	# Get values in range 0 - 1
# 	# tempImage = tempImage / 255.0

# 	return tempImage

# # For test purposes only
# def formatImageAndSave(image):
# 	cv2.imwrite( "/images/beforeFormat.jpg", image )
# 	resultImage = formatImage(image)
# 	cv2.imwrite( "/images/afterFormat.jpg", resultImage )

# 	return resultImage