import cv2
import os
import numpy as np
import time
import sys

from tensorflow import keras

class DataDict:
	def __init__(self,trainDir,testDir):
		self.allTrainPaths, self.allTestPaths, self.allTrainLabels, self.allTestLabels = assemblyPrep(trainDir,testDir)

def getPairs(directory):
	classIndex = 0
	classDirs = os.listdir(sourceDir)
	pairs = []

	for directory in classDirs:
		currentDir = os.path.join(sourceDir,directory)
		for fileName in os.listdir(currentDir):
			currentPath = os.path.join(currentDir,fileName)
			pairs.append([currentPath,classIndex])

		classIndex += 1

def assemblyPrep(trainDir,testDir):
	trainPairs = getPairs(trainDir)
	testPairs = getPairs(testDir)

	trainPaths = trainPairs[:,0]
	trainLabels = trainPairs[:,1]

	testPaths = testPairs[:,0]
	testLabels = testPairs[:,1]

	return trainPaths, trainLabels, testPaths, testLabels

def getImages(paths):
	images = []

	for path in paths:
		temp = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
		images.append( temp )

	return ( np.array(images) / 255.0 )


def imageLoader(paths, labels, batch_size):
	print('start imageLoader batch_size = ' + str(batch_size))
	
	L = len(paths)

	print(L)
	infiniteLoopCount = 0
	#this line is just to make the generator infinite, keras needs it    
	while True:
		print('loopCount = ' + str(infiniteLoopCount))
		infiniteLoopCount += 1

		batch_start = 0
		batch_end = batch_size

		while batch_start < L:
			limit = min(batch_end, L)
			# X = someMethodToLoadImages(paths[batch_start:limit])
			# Y = someMethodToLoadTargets(labels[batch_start:limit])

			print('\nbatch_start = ' + str(batch_start) + ':' + str(limit))
			X = getImages(paths[batch_start:limit])
			Y = labels[batch_start:limit]


			yield (X,Y) #a tuple with two numpy arrays with batch_size samples     

			batch_start += batch_size   
			batch_end += batch_size