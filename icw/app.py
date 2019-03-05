
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
# UPLOAD_IMAGES = os.path.join(STATIC_FOLDER,'images','results')
# RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','results')
####################
# ROOT_FOLDER = os.path.basename('app_files')
# HANDLING_FOLDER = os.path.join(ROOT_FOLDER,'handling','uploads')
# STATIC_FOLDER = os.path.basename('static')
# EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
# RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','results')
##################
# ROOT_FOLDER = os.path.basename('app_files')
# HANDLING_FOLDER = ensurePath( os.path.join(ROOT_FOLDER,'handling','uploads') )
# STATIC_FOLDER = ensurePath( os.path.basename('static') )
# EXAMPLE_IMAGES = ensurePath( os.path.join(STATIC_FOLDER,'images','examples') )
# RESULT_IMAGES = ensurePath( os.path.join(STATIC_FOLDER,'images','results') )
# UPLOAD_IMAGES = ensurePath( os.path.join(STATIC_FOLDER,'images','uploads') )
####################

# UPLOAD_IMAGES = os.path.join(ROOT_FOLDER,'handling','uploads')
# UPLOAD_IMAGES = ROOT_FOLDER
# UPLOAD_IMAGES = os.path.join(ROOT_FOLDER,'static')

# <link rel="stylesheet" href="{{ theme }}">

activeTheme = "static/themes/theme-electricity.css"
# activeTheme = "static/themes/theme-pastel.css"
# activeTheme = "static/themes/theme-sunset.css"

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

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')
### End pages ###

### API ###
@app.route('/testreq')
def testreq():
	#make dict

	# d = 1
	d =	{
		"imageurl": "Ford",
		"model": "Mustang",
		"year": 1964
	}
	return jsonify(d)
	# return json.dumps(d)
	# return "hellotesdffsdfasfa"

@app.route('/static/clientCode/clientHome')
def divert():
	#make dict

	# d = 1
	d =	{
		"imageurl": "Ford",
		"model": "Mustang",
		"year": 1964
	}
	return jsonify(d)
	# return json.dumps(d)
	# return "hellotesdffsdfasfa"

@app.route('/loginrequest', methods=['POST'])
def loginrequest():
	dbQuery.allUsers()

	postArgs = dict(request.values)

	print(type(postArgs['username']))
	print(type(postArgs['password']))

	print(postArgs['username'])
	print(postArgs['password'])
	# print(type(postArgs['notaarg']))

	result = {
		'message': 'Failed login'
	}

	if 'username' in postArgs.keys() and 'password' in postArgs.keys():
		user = dbQuery.namePassUser(postArgs['username'],postArgs['password'])

		if user == None:
			print('Failure')
		else:
			print('Success')
			print(user.toString())

			token = jwt.encode({'userid': user.id}, 'secret', algorithm='HS256')

			result = {
				'token': token.decode('utf-8')
			}

			# print(jwt.encode({'userid': user.id}, 'secret', algorithm='HS256'))

			# var = str(jwt.encode({'userid': user.id}, 'secret', algorithm='HS256'))
			# print(var)

			# print( jwt.decode(var, 'secret', algorithms=['HS256']) )




	# >>> encoded_jwt = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
	# >>> encoded_jwt
	# 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'

	# >>> jwt.decode(encoded_jwt, 'secret', algorithms=['HS256'])
	# {'some': 'payload'}
	# print(request.args)
	# print(request.form)
	# print(request)
	# print(request.data)
	# print(request.values)


	return jsonify(result)

@app.route('/signuprequest', methods=['POST'])
def signuprequest():
	print('signuprequest entered')
	postArgs = dict(request.values)


	print(postArgs['username'])
	print(postArgs['password'])
	print(postArgs['confirmpassword'])


	result = {
		'message': 'Failed signup'
	}

	if 'username' in postArgs.keys() and 'password' in postArgs.keys() and 'confirmpassword' in postArgs.keys():
		print('if 1 true')
		if postArgs['password'] == postArgs['confirmpassword']:
			print('if 2 true')
			if postArgs['username'] != '' and postArgs['password'] != '' and postArgs['confirmpassword'] != '':
				print('if 3 true')

				user = dbModify.insertUser(postArgs['username'],postArgs['password'])



				# print('Return after modify')
				if user == None:
					print('Failure')
				else:
					print('Success')
					print(user.toString())
					result = {
						'token': jwt.encode({'userid': user.id}, 'secret', algorithm='HS256')
					}

				# if user != None:
				# 	print(type(user))
				# print(None)
			else:
				print('Some arguments are blank')
		else:
			print('Passwords dont match')
	else:
		print('Arguments missing')

	# print(request.args)
	# print(request.form)
	# print(request)
	# print(request.data)
	# print(request.values)


	return jsonify(result = {"inputPath": "originalPath," })


### End API ###


# @app.route('/upload')
# def upload():
#     return render_template('upload.html')

# Flask App upload
@app.route('/upload', methods=['POST'])
def upload():

	# request.form['name']
	# request.form.get('token')
	# print(request.form.get('token'))


	# Handles error if image file is not in request
	try:
		file = request.files['image']
	except:
		file = None

	# Renders upload page with error if no file received
	if file == None:
		return None

	# Constructs path for image to be saved to
	originalPath = os.path.join(ORIGINAL_IMAGES,file.filename)

	file.save(originalPath)

	# newImagePath = os.path.join(UPLOAD_IMAGES, file.filename)
	# newImagePath = ''

	classResult = 'test label'

	# TODO: change classify not to take isolate path and have seperate function for making image result
	isolatePath = os.path.join(ISOLATE_IMAGES,file.filename)
	classResult = imageClassification.classifyImage(originalPath,isolatePath)


	#Add database interaction for saving submission
	success = dbModify.insertGuestSubmission(originalPath,isolatePath,classResult)
	print('DB insert: ' + str(success))

	# Renders upload page with classification info and the processed image
	result = {
		"inputPath": originalPath,
		"outputPath": isolatePath,
		"label": classResult
	}
	return jsonify(result)
	# return render_template('upload.html',valid_submit = False)

#TODO: Rename this
@app.route('/galleryImages')
def galleryImages():

	#Redo to also get label
	images = dbQuery.allGalleryImages()
	imagePaths = [{'path': image.path} for image in images]

	return jsonify(imagePaths)


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
	postArgs = dict(request.values)

	result = {
		'message': 'Failed token validation'
	}

	if 'token' in postArgs.keys():
		token = postArgs['token']

		payload = jwt.decode(token.encode('utf-8'), 'secret', algorithms=['HS256'])

		print(payload)

		result = {
			'message': 'Token validated'			
		}

	return jsonify(result)

# # Renders a page with a file upload
# @app.route('/oldupload', methods=['GET','POST'])
# def oldupload():
# 	# Base upload page is rendered if GET request received
# 	if request.method == 'GET':
# 		return render_template('upload.html',valid_submit = False)

# 	# Start processing if POST request received
# 	elif request.method == 'POST':
# 		# Handles error if image file is not in request
# 		try:
# 			file = request.files['image']
# 		except:
# 			file = None

# 		# Renders upload page with error if no file received
# 		if file == None:
# 			return render_template('upload.html',failed_submit = True)

# 		# Constructs path for image to be saved to
# 		# path = os.path.join(UPLOAD_IMAGES, file.filename)
# 		# path = os.path.join(ROOT_FOLDER, UPLOAD_IMAGES, file.filename)
# 		path = os.path.join(HANDLING_FOLDER,file.filename)

# 		file.save(path)


# 		# newImagePath = os.path.join(UPLOAD_IMAGES, file.filename)
# 		newImagePath = ''

# 		classResult = 'test label'

# 		# # Sets the model if not already done and attempts to classify the image
# 		# setModel()
# 		# global model
# 		dest = os.path.join(RESULT_IMAGES,file.filename)

# 		classResult = imageClassification.classifyImage(path,dest)

# 		# # Passes the image path to be processed and the destination directory path
# 		# destDir = app.config['STATIC_FOLDER']
# 		# newImagePath = ip.processImage(path,destDir)
# 		newImagePath = os.path.join(RESULT_IMAGES,file.filename)

# 		# Renders upload page with classification info and the processed image
# 		return render_template('upload.html',valid_submit = True, display_image = newImagePath, class_label = classResult)

# 		# return render_template('upload.html',valid_submit = False)

