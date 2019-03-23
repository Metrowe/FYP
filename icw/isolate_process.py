import numpy as np
import cv2

def isolateImage(imagePath,isolatePath,summaryPath):
	# TODO: add functionality
	isolateImage = cv2.imread(imagePath)
	summaryImage = isolateImage.copy()




	cv2.imwrite(isolatePath,isolateImage)
	cv2.imwrite(summaryPath,summaryImage)

	# TODO: Decide what should be returned, currently success
	# return isolatedImage
	return True