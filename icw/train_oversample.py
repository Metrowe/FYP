from shutil import copyfile
import os
import console_argv

basepath, goal = console_argv.getX(sys.argv, 2, 'basepath goal')

try:
	goal = int(goal)
except ValueError:
	sys.exit('exit: basepath goal, goal to be a number')

classDirs = os.listdir(basepath)

for directory in classDirs:
	currentDir = os.path.join(basepath,directory)
	imageNames = os.listdir(currentDir)

	print(str(len(imageNames)) + ' : ' + directory)

	iteration = 0
	while len(os.listdir(currentDir)) < goal:
		iteration += 1

		i = goal - len(os.listdir(currentDir))
		for name in imageNames:
			if i < 1:
				break
			else:
				source = os.path.join(currentDir,name)
				dest = os.path.join(currentDir,str(iteration) + '_' + name)
				copyfile(source, dest)
				i -= 1