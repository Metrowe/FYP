import time
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui
import os

import console_argv
import sys


def show(image):
	cv2.imshow("", image)
	key = cv2.waitKey(0)

def writeImage(image,path):
	cv2.imwrite(path,image)

def makeSquare(image,padColour):
	height, width, channels = image.shape

	pad = int( ( abs(height - width) ) / 2 )

	if height > width:
		image = cv2.copyMakeBorder(image,0,0,pad,pad,cv2.BORDER_CONSTANT,value=padColour)
	elif width > height:
		image = cv2.copyMakeBorder(image,pad,pad,0,0,cv2.BORDER_CONSTANT,value=padColour)

	return image

def formatImage(image,padColour,finalSize):
	padded = makeSquare(original,padColour)
	resized = cv2.resize(padded,(finalSize,finalSize))

	return resized

def main():
	sourceDir, destDir = console_argv.getX(sys.argv, 2, 'sourceDir destDir')

	finalSize = 200
	padColour = [0,0,0]

	# sourceDir = os.path.join("D:/Datasets","Animals_with_Attributes2","JPEGImages")
	# destDir = os.path.join("D:/Datasets","200X200")

	# Initialise #
	if not os.path.exists(destDir):
		os.mkdir(destDir)

	imageDirs = os.listdir(sourceDir)

	t0 = time.time()
	for directory in imageDirs:
		tx = time.time()
		print(directory)

		sourceImageDir = os.path.join(sourceDir,directory)
		newImageDir = os.path.join(destDir,directory)

		if not os.path.exists(newImageDir):
			os.mkdir(newImageDir)

		for tempImage in os.listdir(sourceImageDir):
			original = cv2.imread( os.path.join(sourceImageDir,tempImage) )

			padded = makeSquare(original,padColour)
			resized = cv2.resize(padded,(finalSize,finalSize))

			newPath = os.path.join(newImageDir,tempImage)
			writeImage(resized,newPath)

		print(time.time() - tx)
		print()

	print("total time = " + str(time.time() - t0))

main()