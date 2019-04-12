import os
import numpy as np
import time

from shutil import copyfile

import console_argv
import sys

def getFold(array,folds,foldNumber):
	size = len(array)
	decimal = 1.0 / folds
	number = number

	start = int(size*decimal*(foldNumber-1))
	end = int(size*decimal*foldNumber)

	return array[start:end]

def main():
	sourceDir, destDir, folds = console_argv.getX(sys.argv, 2, 'sourceDir destDir')

	try:
		folds = int(folds)
	except ValueError:
		sys.exit('exit: expected sourceDir destDir folds and folds to be a number')

	classDirs = os.listdir(sourceDir)

	pairs = []

	for directory in classDirs:
		currentDir = os.path.join(sourceDir,directory)

		for fileName in os.listdir(currentDir):
			currentPath = os.path.join(currentDir,fileName)
			pairs.append([currentPath,directory,fileName])

	if len(pairs) > folds or folds < 1:
		sys.exit('exit: more folds than pairs, can not have empty folds')

	pairs = np.array(pairs)
	np.random.shuffle(pairs)

	for i in range(0,folds):
		tempPairs = getFold(pairs,folds,i+1)
		foldDir = destDir+str(i)

		if not os.path.exists(foldDir):
			os.mkdir(foldDir)

		for pair in tempPairs:

			pairDir = os.path.join(foldDir,pair[1])

			if not os.path.exists(pairDir):
				os.mkdir(pairDir)

			pairPath = os.path.join(pairDir,pair[2])

			copyfile(pair[0], pairPath)

main()