import numpy as np
import cv2
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

def preprocess(image):
	maxDimension = 500
	h, w, channels = image.shape

	if h > w:
		newH = maxDimension
		newW = (newH/h) * w
	if w > h:
		newW = maxDimension
		newH = (newW/w) * h
	else:
		newH = maxDimension
		newW = maxDimension
	
	image = cv2.resize(image,(int(newW),int(newH)))
	image = cv2.GaussianBlur(image,(3,3),0)

	return image

def superpixels(image,algorithm,arg1,arg2):
	retval = None

	if algorithm == 'SLIC':
		retval = cv2.ximgproc.createSuperpixelSLIC(	image, cv2.ximgproc.SLIC, arg1, arg2 )
	elif algorithm == 'SLICO':
		retval = cv2.ximgproc.createSuperpixelSLIC(	image, cv2.ximgproc.SLICO, arg1, arg2)
	elif algorithm == 'MSLIC':
		retval = cv2.ximgproc.createSuperpixelSLIC(	image, cv2.ximgproc.MSLIC, arg1	)

	return retval

def getSuperpixelsContours(image,algorithm,arg1,arg2):
	retval = superpixels(image,algorithm,arg1,arg2)
	retval.iterate(10)
	mask = retval.getLabelContourMask(True)

	shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
	mask = cv2.dilate(mask,shape)
	mask_inv = cv2.bitwise_not(mask)
	newmask = mask_inv

	contourTuple = cv2.findContours(newmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	if len(contourTuple) == 3:
		_, contours, _ = contourTuple
	else:
		contours, _ = contourTuple

	return contours

def getBlankImage(image):
	blankImage = image.copy()
	blankImage[:, :] = (0,0,0)

	return blankImage

class InfoContour:
	def __init__(self, contour, size, centre, colour):
		self.contour = contour
		self.size = size
		self.centre = centre
		self.colour = colour

	def distToPoint(self,yx):
		return abs(yx[0] - self.centre[0]) + abs(yx[1] - self.centre[1])

def getClosestContour(infoContours,point):
	closestInc = infoContours[0]
	minDist = infoContours[0].distToPoint(point)

	for inc in infoContours[1:]:
		if inc.distToPoint(point) < minDist:
			closestInc = inc

	return closestInc

def pixelBGR2HSV(pixel):
	newPixel = cv2.cvtColor(np.uint8([[pixel]]),cv2.COLOR_BGR2HSV)
	newPixel = newPixel[0,0]

	return newPixel

def inBGRRange(mainColour, otherColour,range):
	B = abs(mainColour[0] - otherColour[0])
	G = abs(mainColour[1] - otherColour[1])
	R = abs(mainColour[2] - otherColour[2])

	inRange = False
	if np.array([B,G,R]).all() < range:
		inRange = True

	return inRange

def inHRange(mainColour, otherColour,range):
	main = int(pixelBGR2HSV(mainColour)[0])
	other = int(pixelBGR2HSV(otherColour)[0])
	H = abs(main - other)

	inRange = False
	if H < range:
		inRange = True

	return inRange

def getDominantContour(infoContours):
	dominantContour = None

	if len(infoContours) == 1:
		dominantContour = infoContours[0]
	else:
		clone = infoContours.copy()
		maxSize = 0

		for inc in infoContours:
			relativeSize = 0
			for c in clone:
				if inHRange(inc.colour, c.colour,30):
					relativeSize += c.size
		if maxSize < relativeSize:
			maxSize = relativeSize
			dominantContour = inc

	return dominantContour

def crawlToEdge(grid,horizontal):
	rows, cols = grid.shape
	edge = None
	firstAxis = None

	if horizontal:
		firstAxis = rows
	else:
		firstAxis = cols
	
	for i in range(firstAxis):
		skips = 1
		initialContour = None
		arrayEdge = None

		secondAxis = None
		if horizontal:
			secondAxis = grid[i,:]
		else:
			secondAxis = grid[:,i]

		for array in secondAxis:
			if skips < 1:
				break

			if len(array) > 0:
				if initialContour == None:
					initialContour = getDominantContour(array)
					
					if horizontal:
						arrayEdge = initialContour.centre[1]
					else:
						arrayEdge = initialContour.centre[0]
				else:
					currentContour = getDominantContour(array)

					if inHRange(initialContour.colour, currentContour.colour,30):
						if horizontal:
							arrayEdge = initialContour.centre[1]
						else:
							arrayEdge = initialContour.centre[0]
					else:
						break
			else:
				skips -= 1

			if edge == None:
				edge = arrayEdge  
			else:
				if arrayEdge != None:
					if horizontal:
						if edge > arrayEdge:
							edge = arrayEdge 
					else:
						if edge < arrayEdge:
							edge = arrayEdge 

	return edge


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

	# src = cv2.imread(file_name, 1)
	tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
	b, g, r = cv2.split(img)
	rgba = [b,g,r, alpha]
	img = cv2.merge(rgba,4)
	# cv2.imwrite("test.png", dst)

	return img

def getInfoContours(image, contours):
	mainBlank = cv2.cvtColor(getBlankImage(image), cv2.COLOR_BGR2GRAY) 

	infoContours = []

	for contour in contours:
		x,y,w,h = cv2.boundingRect(contour)

		size = w * h
		centre = (y + (h * 0.5), x + (w * 0.5))
		tempColour = np.uint8([0,0,0])
		infoContours.append(InfoContour(contour,size,centre,tempColour))

	totalSize = sum([inc.size for inc in infoContours])
	sizeThreshold = ( totalSize / len(infoContours) ) * 0.5

	for inc in reversed(infoContours):
		if inc.size > sizeThreshold:
			tempBlank = mainBlank.copy()

			cv2.drawContours(tempBlank, [inc.contour], 0, color=255, thickness=-1)
			pts = np.where(tempBlank == 255)

			colours = image[pts[0], pts[1]]

			clt = KMeans(n_clusters=1)
			clt.fit(colours)

			inc.colour = clt.cluster_centers_[0].astype("uint8").tolist()
		else:
			infoContours.remove(inc)

	return infoContours

def assignToGrid(image,infoContours):
	height, width, channels = image.shape
	pixelLength = int( (height + width) / 10 )
	rows = int( height / pixelLength ) + 1
	cols = int( width / pixelLength ) + 1

	grid = np.empty([rows, cols], dtype=object )
	gridheight, gridwidth = grid.shape

	for y in range(gridheight):
		for x in range(gridwidth):
			grid[y,x] = []

	for inc in infoContours:
		grid[int(inc.centre[0] / pixelLength),int(inc.centre[1] / pixelLength)].append(inc)

	return grid

def estimateBoundingRect(image,grid):
	height, width, channels = image.shape

	left = crawlToEdge(grid,True)
	top = crawlToEdge(grid,False)

	yAxisFlip = np.flip(grid.copy(), 1)
	xAxisFlip = np.flip(grid.copy(), 0)
	right = crawlToEdge(yAxisFlip,True)
	bottom = crawlToEdge(xAxisFlip,False)

	if left == None:
		left = width * 0.05
	if top == None:
		top = height * 0.05

	if right == None:
		right = width * 0.95
	if bottom == None:
		bottom = height * 0.95

	if int(left) >= int(right):
		left = width * 0.05
		right = width * 0.95

	if int(top) >= int(bottom):
		top = height * 0.05
		bottom = height * 0.95

	return (int(left),int(top),int(right),int(bottom))

def getSummaryImage(image,infoContours):
	summaryImage = getBlankImage(image)
	for inc in infoContours:
		summaryImage = cv2.fillPoly(summaryImage, pts =[inc.contour], color=inc.colour)

	return summaryImage

def isolateImage(imagePath,isolatePath,summaryPath):
	image = cv2.imread(imagePath)

	algorithm = 'SLIC'
	arg1 = 50
	arg2 = 40

	imagePreprocess = preprocess(image)

	contours = getSuperpixelsContours(imagePreprocess,algorithm,arg1,arg2)

	infoContours = getInfoContours(imagePreprocess, contours)

	grid = assignToGrid(imagePreprocess,infoContours)

	rect = estimateBoundingRect(imagePreprocess,grid)

	isolateImage = grabCut(imagePreprocess,rect)
	summaryImage = getSummaryImage(imagePreprocess,infoContours)

	cv2.imwrite(isolatePath,isolateImage)
	cv2.imwrite(summaryPath,summaryImage)


	return True