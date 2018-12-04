import cv2
import numpy as np
import os
import random
import string

# Random string generator for labeling files
def getRandomString(length):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))

# Subject of image is extracted before being saved and returning the new path
def processImage(imagePath,destDir):
	src = imagePath
	original = cv2.imread(src)

	tempImage = original.copy()

	# The bounding box of the image is calculated
	rect = getRectangle(tempImage)

	# The backgound is removed using the bounding box with the grabcut algorithm
	displayImage = grabCut(tempImage,rect)

	# New path is generated
	newPath = os.path.join(destDir, getRandomString(5) + ".png")

	# File is written to the specified path
	cv2.imwrite(newPath,displayImage)
	return newPath

# The image is thresholded and a binary image returned
def binaryThresh(image):
	# Image is converted to gray
	G = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Threshod areas in the 0 - 200 grayscale range
	ret,thresh = cv2.threshold(G,0,200,cv2.THRESH_BINARY)

	return thresh

def getRectangle(image):
	# Find a mask using a simple threshold
	mask = binaryThresh(image)

	# Shape and co-ordinate variables are initialised
	height, width, channels = image.shape
	y1 = y2 = 0
	x1 = x2 = 0

	# finds the top and bottom y values of the thresholded image
	for y in range(0,height):
		if np.sum(mask[y,:]) > 0:

			if y2 == 0:
				y1 = y
			y2 = y

	# finds the leftmost and rightmost x values of the thresholded image
	for x in range(0,width):
		if np.sum(mask[:,x]) > 0:

			if x2 == 0:
				x1 = x
			x2 = x

	# Bounding box is assembled and returned
	rect = (x1,y1,x2,y2)

	return rect

def grabCut(img,rect):
	# mask equal to size of image is calculated
	mask = np.zeros(img.shape[:2],np.uint8)

	# Masks for background and foreground highlights are calculated
	#	Currently no highlights set
	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)

	# Values are passed into the grabcut algorithm and it attempts to mark the foreground pixels in the mask
	cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	# The mask is simplified
	mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	#The simplified mask is applied to the image to remove the background
	img = img*mask2[:,:,np.newaxis]

	return img