
# A very simple Flask Hello World app for you to get started with...
import time
import tensorflow
import cv2
import os
from flask import Flask, render_template, request, jsonify
import imageClassification
import tempConfig
import json

import jwt

import database_modify as dbModify
import database_query as dbQuery
from database_connection import Session

import random
import string
import time

# Random string generator for labeling files
def getUniqueTimeStamp():
# def RENAMEGETFILENAME():
	t = time.localtime(time.time())

	timeString = '{}-{}-{}_{}-{}-{}'.format(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
	randomString = ''.join(random.choice(string.ascii_letters) for i in range(5))
	return timeString + '_' + randomString

# import data

# import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# def ensurePath(path):
# 	if not os.path.exists(path):
# 		os.makedirs(path)

# 	return path

# app = Flask(__name__,template_folder='app_files/templates',static_folder='app_files/static')
app = Flask(__name__,template_folder='templates',static_folder='static')

# if 'FYP' in os.listdir('.'):
# 	tempConfig.BASE_FOLDER = os.path.join('FYP','icw')
# 	ROOT_FOLDER = os.path.join('FYP','icw','app_files')
# else:
# 	tempConfig.BASE_FOLDER = os.path.basename('.')
# 	ROOT_FOLDER = os.path.basename('app_files')

HANDLING_FOLDER = os.path.join('handling','uploads')
STATIC_FOLDER = os.path.basename('static')
EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
ORIGINAL_IMAGES = os.path.join(STATIC_FOLDER,'images','original')
ISOLATE_IMAGES = os.path.join(STATIC_FOLDER,'images','isolate')
####################
# ROOT_FOLDER = os.path.basename('app_files')
# HANDLING_FOLDER = os.path.join('handling','uploads')
# STATIC_FOLDER = os.path.basename('static')
# EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
# UPLOAD_IMAGES = os.path.join(STATIC_FOLDER,'images','responses')
# RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','responses')
####################
# ROOT_FOLDER = os.path.basename('app_files')
# HANDLING_FOLDER = os.path.join(ROOT_FOLDER,'handling','uploads')
# STATIC_FOLDER = os.path.basename('static')
# EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
# RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','responses')
##################
# ROOT_FOLDER = os.path.basename('app_files')
# HANDLING_FOLDER = ensurePath( os.path.join(ROOT_FOLDER,'handling','uploads') )
# STATIC_FOLDER = ensurePath( os.path.basename('static') )
# EXAMPLE_IMAGES = ensurePath( os.path.join(STATIC_FOLDER,'images','examples') )
# RESULT_IMAGES = ensurePath( os.path.join(STATIC_FOLDER,'images','responses') )
# UPLOAD_IMAGES = ensurePath( os.path.join(STATIC_FOLDER,'images','uploads') )
####################

# UPLOAD_IMAGES = os.path.join(ROOT_FOLDER,'handling','uploads')
# UPLOAD_IMAGES = ROOT_FOLDER
# UPLOAD_IMAGES = os.path.join(ROOT_FOLDER,'static')

# <link rel="stylesheet" href="{{ theme }}">

activeTheme = "static/themes/theme-electricity.css"
# activeTheme = "static/themes/theme-pastel.css"
# activeTheme = "static/themes/theme-sunset.css"



def encodeToken(payload):
	return jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
	# token = jwt.encode({'userid': user.id}, 'secret', algorithm='HS256').decode('utf-8')

	# response = {
	# 	'token': token.decode('utf-8')
	# }

def decodeToken(token):
	try:
		payload = jwt.decode(token.encode('utf-8'), 'secret', algorithms=['HS256'])
	except jwt.exceptions.DecodeError:
		print('failed decode')
		payload = None

	return payload
	# return jwt.decode(token.encode('utf-8'), 'secret', algorithms=['HS256'])

### TODO: add to external files ##
def responseError(text):
	return {
		'error': text
	}

def validString(text):
	if not (' ' in text) and not ('	' in text)and text != '':
		return True
	else:
		return False
### end todo

### Management ### rename section
@app.teardown_appcontext
def cleanup(resp_or_exc):
	Session.remove()
### End Management ###

### Pages ###
@app.route('/')
def home():
    local_time = 'Local time:' + time.ctime(time.time())

    # return local_time
    # return render_template('index.html')

    # return render_template('index.html',exampleImage = os.path.join(EXAMPLE_IMAGES,'deereg.jpg'))
    # return render_template('home.html',theme = activeTheme)
    return render_template('home.html')
    # return render_template('home.html',theme = activeTheme,exampleImage = os.path.join(EXAMPLE_IMAGES,'deereg.jpg'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/gallery')
def gallery():
	return render_template('gallery.html')

@app.route('/myuploads')
def myuploads():
	return render_template('myuploads.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/adminapproval')
def adminapproval():
	return render_template('adminapproval.html')
### End pages ###

### API ###
@app.route('/loginrequest', methods=['POST'])
def loginrequest():
	dbQuery.allUsers()

	postArgs = dict(request.values)

	response = responseError('Login denied')

	if 'username' in postArgs.keys() and 'password' in postArgs.keys():

		if validString(postArgs['username']) and validString(postArgs['password']):

			user = dbQuery.namePassUser(postArgs['username'],postArgs['password'])

			if user != None:
				dbQuery.allUsers()
				response = {
					'token': encodeToken({'userid': user.id})
				}
				# token = jwt.encode({'userid': user.id}, 'secret', algorithm='HS256')

				# response = {
				# 	'token': token.decode('utf-8')
				# }
			else:
				response = responseError('Username or password is incorrect')

	return jsonify(response)

@app.route('/signuprequest', methods=['POST'])
def signuprequest():
	postArgs = dict(request.values)

	response = responseError('Signup denied')

	if 'username' in postArgs.keys() and 'password' in postArgs.keys() and 'confirmpassword' in postArgs.keys():

		if postArgs['password'] == postArgs['confirmpassword']:

			if validString(postArgs['username']) and validString(postArgs['password']):
				user = dbModify.insertUser(postArgs['username'],postArgs['password'])

				if user != None:
					# response = {
					# 	'token': jwt.encode({'userid': user.id}, 'secret', algorithm='HS256')
					# }

					response = {
						'token': encodeToken({'userid': user.id})
					}
				else:
					response = responseError('Username is already taken')

	return jsonify(response)

@app.route('/givefeedbackrequest', methods=['POST'])
def giveFeedbackRequest():
	postArgs = dict(request.values)

	# reponse = responseError('Submit feedback denied')
	reponse = responseError('Feedback request denied')

	if 'submissionToken' in postArgs.keys() and 'rateClassify' in postArgs.keys() and 'rateIsolate' in postArgs.keys() and 'commentResult' in postArgs.keys() and 'commentSite' in postArgs.keys():
		payload = decodeToken(postArgs['submissionToken'])

		if payload != None:
			submission = dbModify.updateFeedback(payload['submissionId'],postArgs['rateClassify'],postArgs['rateIsolate'],postArgs['commentResult'],postArgs['commentSite'])
			print('DB insert: ' + str(submission != None))
			print('ID: ' + str(submission.id))

			response = {
				'message': 'Feedback submission success'
			}
		else:
			response = responseError('Invalid submission token')

	return jsonify(response)

@app.route('/upload', methods=['POST'])
def upload():
	# Handles error if image file is not in request
	try:
		file = request.files['image']
	except:
		file = None

	headers = dict(request.headers)
	postArgs = dict(request.values)
	files = dict(request.files)

	response = responseError('Upload request invalid')

	# Renders upload page with error if no file received
	if file != None:
		# Constructs path for image to be saved to
		filename = getUniqueTimeStamp() + '.png'
		originalPath = os.path.join(ORIGINAL_IMAGES,filename)
		isolatePath = os.path.join(ISOLATE_IMAGES,filename)
		file.save(originalPath)

		# TODO: change classify not to take isolate path and have seperate function for making image response
		classResult = imageClassification.classifyImage(originalPath,isolatePath)
		# classResult = imageClassification.classifyImage(originalPath)
		# success = imageIsolation.isolateImage(isolatePath)

		if 'Authorization' in headers.keys():
			token = headers['Authorization']
			payload = decodeToken(token)

			if payload != None and 'userid' in payload.keys() and dbQuery.idUserExist(payload['userid']):
				userId = payload['userid']
				submissionId = dbModify.insertUserSubmission(originalPath,isolatePath,classResult,userId,True)
				# Renders upload page with classification info and the processed image
				response = {
					'inputPath': originalPath,
					'outputPath': isolatePath,
					'label': classResult,
					'submissionToken': encodeToken({'submissionId': submissionId})
				}
			else:
				response = responseError('Failed Authorization')
		else:
			submissionId = dbModify.insertGuestSubmission(originalPath,isolatePath,classResult,True)
			# Renders upload page with classification info and the processed image
			response = {
				'inputPath': originalPath,
				'outputPath': isolatePath,
				'label': classResult,
				'submissionToken': encodeToken({'submissionId': submissionId})
			}

	return jsonify(response)

#####################################################################################################
@app.route('/galleryrequest', methods=['POST'])
def galleryRequest():
	postArgs = dict(request.values)

	response = responseError('Gallery request invalid')

	# filterGalleryImages(original,isolate,label)

	# formData.append('type', type);
	# formData.append('label', label);


	if 'type' in postArgs.keys() and 'label' in postArgs.keys():
		print('postArgs[label] : ' + str(postArgs['label']))
		print('type : ' + str(type(postArgs['label'])))

		label = postArgs['label']

		if postArgs['label'] == '':
			label = None

		# if postArgs['type'] == 'All':
		# 	images = dbQuery.filterGalleryImages(True,True,label)
		# 	response = [{'path': image.path} for image in images]
		# elif postArgs['type'] == 'Original':
		# 	images = dbQuery.filterGalleryImages(True,False,label)
		# 	response = [{'path': image.path} for image in images]
		# elif postArgs['type'] == 'Isolate':
		# 	images = dbQuery.filterGalleryImages(False,True,label)
		# 	response = [{'path': image.path} for image in images]
		# else:
		# 	response = responseError('Invalid type')

		if postArgs['type'] in ['All','Original','Isolate']:
			if postArgs['type'] == 'All':
				images = dbQuery.filterGalleryImages(True,True,label)
			elif postArgs['type'] == 'Original':
				images = dbQuery.filterGalleryImages(True,False,label)
			elif postArgs['type'] == 'Isolate':
				images = dbQuery.filterGalleryImages(False,True,label)

			response = [{'path': image.path,'label': image.submission.animalLabel} for image in images]

		else:
			response = responseError('Invalid type')
 


		# if postArgs['password'] == postArgs['confirmpassword']:

		# 	if validString(postArgs['username']) and validString(postArgs['password']):
		# 		user = dbModify.insertUser(postArgs['username'],postArgs['password'])

		# 		if user != None:
		# 			response = {
		# 				'token': jwt.encode({'userid': user.id}, 'secret', algorithm='HS256')
		# 			}
		# 		else:
		# 			reponse = responseError('Username is already taken')

	return jsonify(response)

@app.route('/myuploadsrequest', methods=['POST'])
def myuploadsRequest():
	headers = dict(request.headers)
	postArgs = dict(request.values)

	response = responseError('Myuploads request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		# payload = jwt.decode(token.encode('utf-8'), 'secret', algorithms=['HS256'])
		payload = decodeToken(token)

		print(payload)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserExist(payload['userid']):
			id = payload['userid']

			if 'type' in postArgs.keys() and 'label' in postArgs.keys():
				print('postArgs[label] : ' + str(postArgs['label']))
				print('type : ' + str(type(postArgs['label'])))

				label = postArgs['label']

				if postArgs['label'] == '':
					label = None

				if postArgs['type'] in ['All','Original','Isolate']:
					if postArgs['type'] == 'All':
						images = dbQuery.filterMyuploadsImages(True,True,label,id)
					elif postArgs['type'] == 'Original':
						images = dbQuery.filterMyuploadsImages(True,False,label,id)
					elif postArgs['type'] == 'Isolate':
						images = dbQuery.filterMyuploadsImages(False,True,label,id)

					response = [{'path': image.path,'label': image.submission.animalLabel} for image in images]

				else:
					response = responseError('Invalid type')
	# else:
	# 	response = responseError('Invalid type')


		# if postArgs['password'] == postArgs['confirmpassword']:

		# 	if validString(postArgs['username']) and validString(postArgs['password']):
		# 		user = dbModify.insertUser(postArgs['username'],postArgs['password'])

		# 		if user != None:
		# 			response = {
		# 				'token': jwt.encode({'userid': user.id}, 'secret', algorithm='HS256')
		# 			}
		# 		else:
		# 			reponse = responseError('Username is already taken')

	return jsonify(response)


@app.route('/adminapprovalrequest', methods=['POST'])
def adminapprovalRequest():
	headers = dict(request.headers)

	response = responseError('Adminapproval request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		payload = decodeToken(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):
			# id = payload['userid']

			submissions = dbQuery.reviewSubmissions()


			response = []

			for submission in submissions:


				id = submission.id
				originalPath = submission.originalImage.path
				isolatePath = submission.isolateImage.path
				label = submission.animalLabel

				rateClassify = None
				rateIsolate = None
				commentResult = None
				commentSite = None

				feedback = submission.subFeedback

				if feedback != None:
					rateClassify = feedback.rateClassify
					rateIsolate = feedback.rateIsolate
					commentResult = feedback.commentResult
					commentSite = feedback.commentSite

				response.append({
					'id': id,\
					'originalPath': originalPath,\
					'isolatePath': isolatePath,\
					'label': label,\
					'rateClassify': rateClassify,\
					'rateIsolate': rateIsolate,\
					'commentResult': commentResult,\
					'commentSite': commentSite\
				})

			# response = [{
			# 	'id': submission.id,\
			# 	'originalPath': submission.originalImage.path,\
			# 	'isolatePath': submission.isolateImage.path,\
			# 	'label': submission.animalLabel,\
			# 	'rateClassify': submission.subFeedback.rateClassify,\
			# 	'rateIsolate': submission.subFeedback.rateIsolate,\
			# 	'commentResult': submission.subFeedback.commentResult,\
			# 	'commentSite': submission.subFeedback.commentSite\
			# } for submission in submissions]


	return jsonify(response)

			# if 'type' in postArgs.keys() and 'label' in postArgs.keys():
			# 	print('postArgs[label] : ' + str(postArgs['label']))
			# 	print('type : ' + str(type(postArgs['label'])))

			# 	label = postArgs['label']

			# 	if postArgs['label'] == '':
			# 		label = None

			# 	if postArgs['type'] in ['All','Original','Isolate']:
			# 		if postArgs['type'] == 'All':
			# 			images = dbQuery.filterMyuploadsImages(True,True,label,id)
			# 		elif postArgs['type'] == 'Original':
			# 			images = dbQuery.filterMyuploadsImages(True,False,label,id)
			# 		elif postArgs['type'] == 'Isolate':
			# 			images = dbQuery.filterMyuploadsImages(False,True,label,id)

			# 		response = [{'path': image.path,'label': image.submission.animalLabel} for image in images]

			# 	else:
			# 		response = responseError('Invalid type')
#####################################################################################################
@app.route('/setapprovalrequest', methods=['POST'])
def setapprovalRequest():
	postArgs = dict(request.values)
	headers = dict(request.headers)

	response = responseError('Setapproval request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		payload = decodeToken(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):

			if 'approval' in postArgs.keys() and 'submissionId' in postArgs.keys():
				approval = postArgs['approval']

				if approval in ['true','false']:
					if approval == 'true':
						approval = True
					elif approval == 'false':
						approval = False
					submission = dbModify.updateModApproval(postArgs['submissionId'],approval)

					response = { 'message': 'id' }


	return jsonify(response)

@app.route('/deletesubmissionrequest', methods=['POST'])
def deleteSubmissionRequest():
	postArgs = dict(request.values)
	headers = dict(request.headers)

	response = responseError('Delete submission request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		payload = decodeToken(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):

			if 'submissionId' in postArgs.keys():
				success = str(dbModify.deleteSubmission(postArgs['submissionId']))

				response = { 'message': 'delete ' + success }


	return jsonify(response)


# @app.route('/galleryImages')
# def galleryImages():

# 	#Redo to also get label
# 	images = dbQuery.allGalleryImages()
# 	imagePaths = [{'path': image.path} for image in images]

# 	return jsonify(imagePaths)
# ######################################################################################################
# @app.route('/galleryImages')
# def galleryImages():

# 	#Redo to also get label
# 	images = dbQuery.allGalleryImages()
# 	imagePaths = [{'path': image.path} for image in images]

# 	return jsonify(imagePaths)
### End API ###




#TODO: Rename this



@app.route('/oldupload', methods=['GET','POST'])
def oldupload():
	print('called oldupload')


# @app.route('/ggggg',methods=['POST'])
# def ggggg():

# 	temp = {'path': image.path}

# 	console.log('ooooooooo')

# 	return jsonify(temp)

@app.route('/ggggg', methods=['POST'])
def ggggg():
	# postArgs = dict(request.values)
	headers = dict(request.headers)

	# if 'Authorization' in headers:
	# 	print(headers)
	# 	print(headers['Authorization'])
	# else:
	# 	print('auth not in header')

	response = {
		'message': 'Failed token validation'
	}

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		# payload = jwt.decode(token.encode('utf-8'), 'secret', algorithms=['HS256'])
		payload = decodeToken(token)

		print(payload)

		response = {
			'message': 'Token validated'			
		}

	return jsonify(response)