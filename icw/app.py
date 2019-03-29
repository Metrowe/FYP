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
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

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
	file = None
	if 'image' in request.files.keys():
		file = request.files['image']

	token = web_handling.getAuthorization(request.headers)

	permissionGalleryString, permissionDatasetString = web_handling.getArgs(request.values, 'permissionGallery', 'permissionDataset')
	permissionGallery = web_handling.stringToBool(permissionGalleryString)
	permissionDataset = web_handling.stringToBool(permissionDatasetString)


	response = web_handling.responseError('Upload request invalid')

	# Renders upload page with error if no file received
	if file != None and permissionGallery != None and permissionDataset != None:
		
		# Constructs path for image to be saved to
		filename = os_fileManagement.getUniqueTimeStamp() + '.png'
		originalPath = os.path.join(ORIGINAL_IMAGES,filename)
		isolatePath = os.path.join(ISOLATE_IMAGES,filename)
		summaryPath = os.path.join(SUMMARY_IMAGES,filename)
		file.save(originalPath)

		if os_fileManagement.validImageFile(originalPath):
			animalLabel = None
			isolateSuccess = False

			try:
				animalLabel = classify_process.classifyImage(originalPath)
			except Exception as e:
				logf = open('zClassifyError.log', 'a')
				logf.write('Failed classify [{0}]: {1}\n'.format(filename,str(e)))

			try:
				isolateSuccess = isolate_process.isolateImage(originalPath,isolatePath,summaryPath)
			except Exception as e:
				logf = open('zIsolateError.log', 'a')
				logf.write('Failed isolate [{0}]: {1}\n'.format(filename,str(e)))

			if animalLabel != None and isolateSuccess:
				if token != None:
					payload = web_tokens.decode(token)

					if payload != None and 'userid' in payload.keys() and dbQuery.idUserExist(payload['userid']):
						userId = payload['userid']
						submissionId = dbModify.insertUserSubmission(originalPath,isolatePath,summaryPath,animalLabel,permissionGallery,permissionDataset,userId)

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
			else:
				response = web_handling.responseError('Failed isolate and classify')
		else:
			response = web_handling.responseError('Invalid file, only images are accepted')

	return jsonify(response)

@app.route('/loginrequest', methods=['POST'])
def loginrequest():
	username, password = web_handling.getArgs(request.values, 'username', 'password')
	username = web_handling.getValidString(username)
	password = web_handling.getValidString(password)

	response = web_handling.responseError('Login denied')

	if username != None and password != None:

		user = dbQuery.namePassUser(username,password)

		if user != None:
			response = {
				'token': web_tokens.encode({'userid': user.id})
			}
		else:
			response = web_handling.responseError('Username or password is incorrect')

	return jsonify(response)

@app.route('/signuprequest', methods=['POST'])
def signuprequest():
	username, password, confirmpassword = web_handling.getArgs(request.values, 'username', 'password','confirmpassword')
	username = web_handling.getValidString(username)
	password = web_handling.getValidString(password)
	confirmpassword = web_handling.getValidString(confirmpassword)

	response = web_handling.responseError('Signup denied')

	if username != None and password != None and password == confirmpassword:
		user = dbModify.insertUser(username,password)

		if user != None:
			response = {
				'token': web_tokens.encode({'userid': user.id})
			}
		else:
			response = web_handling.responseError('Username is already taken')

	return jsonify(response)

@app.route('/givefeedbackrequest', methods=['POST'])
def giveFeedbackRequest():
	submissionToken, rateClassify, rateIsolate, commentResult, commentSite = web_handling.getArgs(request.values, 'submissionToken','rateClassify','rateIsolate','commentResult','commentSite')

	response = web_handling.responseError('Feedback request denied')

	if submissionToken != None and rateClassify != None and rateIsolate != None and commentResult != None and commentSite != None:
		payload = web_tokens.decode(submissionToken)

		if payload != None and 'submissionId' in payload.keys():
			submission = dbModify.updateFeedback(payload['submissionId'],rateClassify, rateIsolate, commentResult, commentSite)

			print('payload[submissionId]:',payload['submissionId'])
			print('submission',submission)
			print('submission.feedback',submission.feedback)

			response = {
				'message': 'Feedback submission success'
			}
		else:
			response = web_handling.responseError('Invalid submission token')

	return jsonify(response)

@app.route('/galleryrequest', methods=['POST'])
def galleryRequest():
	category, label = web_handling.getArgs(request.values, 'category', 'label')

	response = web_handling.responseError('Gallery request invalid')

	if category != None and label != None:
		if category == '' or category == 'all':
			category = None

		if label == '':
			label = None

		images = dbQuery.filterGalleryImages(category,label)

		response = [{'path': image.path,'label': image.submission.animalLabel} for image in images]

	return jsonify(response)

@app.route('/myuploadsrequest', methods=['POST'])
def myuploadsRequest():
	token = web_handling.getAuthorization(request.headers)
	category, label = web_handling.getArgs(request.values, 'category', 'label')


	response = web_handling.responseError('Myuploads request invalid')

	if token != None:
		payload = web_tokens.decode(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserExist(payload['userid']):
			id = payload['userid']

			if category != None and label != None :
				if category == '' or category == 'all':
					category = None

				if label == '':
					label = None

				images = dbQuery.filterMyuploadsImages(category,label,id)

				response = [{'path': image.path,'label': image.submission.animalLabel} for image in images]

	return jsonify(response)


@app.route('/adminapprovalrequest', methods=['POST'])
def adminapprovalRequest():
	token = web_handling.getAuthorization(request.headers)

	response = web_handling.responseError('Adminapproval request invalid')

	if token != None:
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
				permissionGallery = submission.permissionGallery

				rateClassify = None
				rateIsolate = None
				commentResult = None
				commentSite = None

				feedback = submission.feedback

				print('submission.feedback:',submission.feedback)
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
					'username': username,\
					'permissionGallery': permissionGallery\
				})

	return jsonify(response)

@app.route('/setapprovalrequest', methods=['POST'])
def setApprovalRequest():
	token = web_handling.getAuthorization(request.headers)
	submissionId, approval, newLabel = web_handling.getArgs(request.values, 'submissionId', 'approval', 'newLabel')
	approval = web_handling.stringToBool(approval)


	# postArgs = (request.values).to_dict()
	# headers = dict(request.headers)

	response = web_handling.responseError('Setapproval request invalid')

	if token != None:
		payload = web_tokens.decode(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):

			if submissionId != None and approval != None:

				# if newLabel != None and newLabel != '':
				# 	newLabel = postArgs['newLabel']

				submission = dbModify.updateModApproval(submissionId,approval,newLabel)

				if submission != None:
					response = { 'message': submissionId }

	return jsonify(response)

@app.route('/deletesubmissionrequest', methods=['POST'])
def deleteSubmissionRequest():
	# postArgs =(request.values).to_dict()
	# headers = dict(request.headers)

	token = web_handling.getAuthorization(request.headers)
	submissionId, newLabel = web_handling.getArgs(request.values, 'submissionId', 'newLabel')

	response = web_handling.responseError('Delete submission request invalid')

	if token != None:
		payload = web_tokens.decode(token)

		if payload != None and 'userid' in payload.keys() and dbQuery.idUserAdmin(payload['userid']):

			if submissionId != None:
				success = str(dbModify.deleteSubmission(submissionId))

				response = { 'message': 'delete ' + success }

	return jsonify(response)