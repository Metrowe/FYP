
# A very simple Flask Hello World app for you to get started with...
import time
import tensorflow
import cv2
import os
from flask import Flask, render_template, request, jsonify
import imageClassification
import tempConfig
import json

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

####################
# ROOT_FOLDER = os.path.basename('app_files')
HANDLING_FOLDER = os.path.join('handling','uploads')
STATIC_FOLDER = os.path.basename('static')
EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','results')
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

### Pages ###
@app.route('/')
def home():
    local_time = 'Local time:' + time.ctime(time.time())

    # return local_time
    # return render_template('index.html')

    # return render_template('index.html',exampleImage = os.path.join(EXAMPLE_IMAGES,'deereg.jpg'))
    return render_template('home.html',theme = activeTheme)
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

### End API ###


# @app.route('/upload')
# def upload():
#     return render_template('upload.html')

# Flask App upload
# Renders a page with a file upload
@app.route('/upload', methods=['GET','POST'])
def upload():
	# Base upload page is rendered if GET request received
	if request.method == 'GET':
		return render_template('upload.html',valid_submit = False)

	# Start processing if POST request received
	elif request.method == 'POST':
		# Handles error if image file is not in request
		try:
			file = request.files['image']
		except:
			file = None

		# Renders upload page with error if no file received
		if file == None:
			return render_template('upload.html',failed_submit = True)

		# Constructs path for image to be saved to
		# path = os.path.join(UPLOAD_IMAGES, file.filename)
		# path = os.path.join(ROOT_FOLDER, UPLOAD_IMAGES, file.filename)
		path = os.path.join(HANDLING_FOLDER,file.filename)

		file.save(path)


		# newImagePath = os.path.join(UPLOAD_IMAGES, file.filename)
		newImagePath = ''

		classResult = 'test label'

		# # Sets the model if not already done and attempts to classify the image
		# setModel()
		# global model
		dest = os.path.join(RESULT_IMAGES,file.filename)

		classResult = imageClassification.classifyImage(path,dest)

		# # Passes the image path to be processed and the destination directory path
		# destDir = app.config['STATIC_FOLDER']
		# newImagePath = ip.processImage(path,destDir)
		newImagePath = os.path.join(RESULT_IMAGES,file.filename)

		# Renders upload page with classification info and the processed image
		return render_template('upload.html',valid_submit = True, display_image = newImagePath, class_label = classResult)

		# return render_template('upload.html',valid_submit = False)

