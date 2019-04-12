import os
import numpy as np
import time

from shutil import copyfile

import console_argv
import sys

def main():
	sourceDir, folds, testFold = console_argv.getX(sys.argv, 3, 'sourceDir folds testFold')

	try:
		folds = int(folds)
		testFold = int(testFold)
	except ValueError:
		sys.exit('exit: expected sourceDir folds testFold, folds and testFold to be numbers')


	trainDir = sourceDir + 'TrainMinus' +str(testFold)
	if os.path.exists(trainDir):
		sys.exit('exit: please provide a different sourceDir or testFold',trainDir,'already exists')

	for i in range(folds):
		if i != testFold:
			foldDir = sourceDir + str(i)
			if not os.path.exists(foldDir):
				sys.exit('exit:',foldDir,'does not exist')

			for directory in os.listdir(foldDir):
				categoryDir = os.path.join(directory,directory)
				destDir = os.path.join(trainDir,directory)

				for fileName in os.listdir(categoryDir)
					currentPath = os.path.join(categoryDir,fileName)
					destPath = os.path.join(destDir,fileName)
					copyfile(currentPath, destPath)

main()