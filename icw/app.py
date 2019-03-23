# Main flask imports
from flask import Flask, render_template, request, jsonify

# Misc imports
import tensorflow
import cv2
import os
import json
import jwt

import classify_process
import isolate_process

from database_connection import Session
import database_modify as dbModify
import database_query as dbQuery

import web_tokens
import web_handling
import os_fileManagement

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

app = Flask(__name__,template_folder='templates',static_folder='static')

STATIC_FOLDER = os.path.basename('static')
IMAGE_FOLDER = os.path.join(STATIC_FOLDER,'images')
EXAMPLE_IMAGES = os.path.join(IMAGE_FOLDER,'examples')
ORIGINAL_IMAGES = os.path.join(IMAGE_FOLDER,'original')
ISOLATE_IMAGES = os.path.join(IMAGE_FOLDER,'isolate')
SUMMARY_IMAGES = os.path.join(IMAGE_FOLDER,'summary')

### Management ### rename section
@app.teardown_appcontext
def cleanup(resp_or_exc):
	Session.remove()
### End Management ###

### Pages ###
@app.route('/')
def home():
    return render_template('home.html')

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
@app.route('/uploadRequest', methods=['POST'])
def uploadRequest():
	# Handles error if image file is not in request
	try:
		file = request.files['image']
	except:
		file = None

	headers = dict(request.headers)
	postArgs = dict(request.values)
	files = dict(request.files)

	response = web_handling.responseError('Upload request invalid')

	# Renders upload page with error if no file received
	if file != None and 'permissionGallery' in postArgs.keys() and 'permissionDataset' in postArgs.keys():
		permissionGallery = web_handling.stringToBool(postArgs['permissionGallery'])
		permissionDataset = web_handling.stringToBool(postArgs['permissionDataset'])

		if permissionGallery != None and permissionDataset != None:

			# Constructs path for image to be saved to
			filename = os_fileManagement.getUniqueTimeStamp() + '.png'
			originalPath = os.path.join(ORIGINAL_IMAGES,filename)
			isolatePath = os.path.join(ISOLATE_IMAGES,filename)
			summaryPath = os.path.join(SUMMARY_IMAGES,filename)
			file.save(originalPath)

			# TODO: change classify not to take isolate path and have seperate function for making image response
			animalLabel = classify_process.classifyImage(originalPath)
			isolateSuccess = isolate_process.isolateImage(originalPath,isolatePath,summaryPath)

			# classResult = imageClassification.classifyImage(originalPath)
			# success = imageIsolation.isolateImage(isolatePath)

			if 'Authorization' in headers.keys():
				token = headers['Authorization']
				payload = web_tokens.decode(token)

				if payload != None and 'userid' in payload.keys() and dbQuery.idUserExist(payload['userid']):
					userId = payload['userid']
					submissionId = dbModify.insertUserSubmission(originalPath,isolatePath,summaryPath,animalLabel,permissionGallery,permissionDataset,userId)

					# insertUserSubmission(originalPath,isolatePath,summaryPath,animalLabel,permissionGallery,permissionDataset,userId)
					# insertGuestSubmission(originalPath,isolatePath,summaryPath,animalLabel,permissionGallery,permissionDataset)
					# Renders upload page with classification info and the processed image
					response = {
						'inputPath': originalPath,
						'outputPath': isolatePath,
						'summaryPath': summaryPath,
						'label': animalLabel,
						'submissionToken': web_tokens.encode({'submissionId': submissionId})
					}
				else:
					response = web_handling.responseError('Failed Authorization')
			else:
				submissionId = dbModify.insertGuestSubmission(originalPath,isolatePath,summaryPath,animalLabel,permissionGallery,permissionDataset)
				# Renders upload page with classification info and the processed image
				response = {
					'inputPath': originalPath,
					'outputPath': isolatePath,
					'summaryPath': summaryPath,
					'label': animalLabel,
					'submissionToken': web_tokens.encode({'submissionId': submissionId})
				}

	return jsonify(response)

@app.route('/loginrequest', methods=['POST'])
def loginrequest():
	dbQuery.allUsers()

	postArgs = dict(request.values)

	response = web_handling.responseError('Login denied')

	if 'username' in postArgs.keys() and 'password' in postArgs.keys():

		if web_handling.validString(postArgs['username']) and web_handling.validString(postArgs['password']):

			user = dbQuery.namePassUser(postArgs['username'],postArgs['password'])

			if user != None:
				dbQuery.allUsers()
				response = {
					'token': web_tokens.encode({'userid': user.id})
				}
			else:
				response = web_handling.responseError('Username or password is incorrect')

	return jsonify(response)

@app.route('/signuprequest', methods=['POST'])
def signuprequest():
	postArgs = dict(request.values)

	response = web_handling.responseError('Signup denied')

	if 'username' in postArgs.keys() and 'password' in postArgs.keys() and 'confirmpassword' in postArgs.keys():

		if postArgs['password'] == postArgs['confirmpassword']:

			if web_handling.validString(postArgs['username']) and web_handling.validString(postArgs['password']):
				user = dbModify.insertUser(postArgs['username'],postArgs['password'])

				if user != None:
					response = {
						'token': web_tokens.encode({'userid': user.id})
					}
				else:
					response = web_handling.responseError('Username is already taken')

	return jsonify(response)

@app.route('/givefeedbackrequest', methods=['POST'])
def giveFeedbackRequest():
	postArgs = dict(request.values)

	reponse = web_handling.responseError('Feedback request denied')

	if 'submissionToken' in postArgs.keys() and 'rateClassify' in postArgs.keys() and 'rateIsolate' in postArgs.keys() and 'commentResult' in postArgs.keys() and 'commentSite' in postArgs.keys():
		payload = web_tokens.decode(postArgs['submissionToken'])

		if payload != None:
			submission = dbModify.updateFeedback(payload['submissionId'],postArgs['rateClassify'],postArgs['rateIsolate'],postArgs['commentResult'],postArgs['commentSite'])
			print('DB insert: ' + str(submission != None))
			print('ID: ' + str(submission.id))

			response = {
				'message': 'Feedback submission success'
			}
		else:
			response = web_handling.responseError('Invalid submission token')

	return jsonify(response)


@app.route('/galleryrequest', methods=['POST'])
def galleryRequest():
	postArgs = dict(request.values)

	response = web_handling.responseError('Gallery request invalid')

	if 'category' in postArgs.keys() and 'label' in postArgs.keys():
		print('postArgs[label] : ' + str(postArgs['label']))
		# print('type : ' + str(type(postArgs['label'])))

		category = postArgs['category']
		label = postArgs['label']

		if category == '' or category == 'all':
			category = None

		if label == '':
			label = None

		print('label',label)


		images = dbQuery.filterGalleryImages(category,label)

		response = [{'path': image.path,'label': image.submission.animalLabel} for image in images]

	return jsonify(response)

@app.route('/myuploadsrequest', methods=['POST'])
def myuploadsRequest():
	headers = dict(request.headers)
	postArgs = dict(request.values)

	response = web_handling.responseError('Myuploads request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']
		payload = web_tokens.decode(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserExist(payload['userid']):
			id = payload['userid']

			if 'category' in postArgs.keys() and 'label' in postArgs.keys():
				category = postArgs['category']
				print('category',category)
				label = postArgs['label']

				if category == '' or category == 'all':
					category = None

				if label == '':
					label = None

				print('label',label)

				images = dbQuery.filterMyuploadsImages(category,label,id)

				response = [{'path': image.path,'label': image.submission.animalLabel} for image in images]

	return jsonify(response)


@app.route('/adminapprovalrequest', methods=['POST'])
def adminapprovalRequest():
	headers = dict(request.headers)

	response = web_handling.responseError('Adminapproval request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		payload = web_tokens.decode(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):
			submissions = dbQuery.reviewSubmissions()

			response = []

			for submission in submissions:
				id = submission.id
				originalPath = next((image.path for image in submission.images if image.type == 'original'), None)
				isolatePath = next((image.path for image in submission.images if image.type == 'isolate'), None)
				summaryPath = next((image.path for image in submission.images if image.type == 'summary'), None)

				label = submission.animalLabel

				rateClassify = None
				rateIsolate = None
				commentResult = None
				commentSite = None

				feedback = submission.feedback
				if feedback != None:
					rateClassify = feedback.rateClassify
					rateIsolate = feedback.rateIsolate
					commentResult = feedback.commentResult
					commentSite = feedback.commentSite

				username = None

				user = submission.user
				if user != None:
					username = user.username

				response.append({
					'id': id,\
					'originalPath': originalPath,\
					'isolatePath': isolatePath,\
					'summaryPath': summaryPath,\
					'label': label,\
					'rateClassify': rateClassify,\
					'rateIsolate': rateIsolate,\
					'commentResult': commentResult,\
					'commentSite': commentSite,\
					'username': username\
				})

	return jsonify(response)

@app.route('/setapprovalrequest', methods=['POST'])
def setApprovalRequest():
	postArgs = dict(request.values)
	headers = dict(request.headers)

	response = web_handling.responseError('Setapproval request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		payload = web_tokens.decode(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):

			if 'approval' in postArgs.keys() and 'submissionId' in postArgs.keys():
				approval = web_handling.stringToBool(postArgs['approval'])

				newLabel = None
				if 'newLabel' in postArgs.keys() and postArgs['newLabel'] != '':
					newLabel = postArgs['newLabel']

				if approval != None:
					submission = dbModify.updateModApproval(postArgs['submissionId'],approval,newLabel)

					response = { 'message': 'id' }


	return jsonify(response)

@app.route('/deletesubmissionrequest', methods=['POST'])
def deleteSubmissionRequest():
	postArgs = dict(request.values)
	headers = dict(request.headers)

	response = web_handling.responseError('Delete submission request invalid')

	if 'Authorization' in headers.keys():
		token = headers['Authorization']

		payload = web_tokens.decode(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):

			if 'submissionId' in postArgs.keys():
				success = str(dbModify.deleteSubmission(postArgs['submissionId']))

				response = { 'message': 'delete ' + success }

	return jsonify(response)