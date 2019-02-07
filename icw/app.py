
# A very simple Flask Hello World app for you to get started with...
import time
import tensorflow
import cv2
import os
from flask import Flask, render_template, request
import imageClassification

app = Flask(__name__,template_folder="app_files/templates",static_folder="app_files/static")

ROOT_FOLDER = os.path.basename('app_files')

STATIC_FOLDER = os.path.basename('static')

EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','results')

UPLOAD_IMAGES = os.path.join(STATIC_FOLDER,'images','uploads')



# UPLOAD_IMAGES = os.path.join(ROOT_FOLDER,'handling','uploads')
# UPLOAD_IMAGES = ROOT_FOLDER
# UPLOAD_IMAGES = os.path.join(ROOT_FOLDER,'static')


@app.route('/')
def index():
    local_time = "Local time:" + time.ctime(time.time())

    # return local_time
    return render_template("index.html",exampleImage = os.path.join(EXAMPLE_IMAGES,'deereg.jpg'))
    # return render_template("index.html")

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
		path = os.path.join(ROOT_FOLDER,"handling",file.filename)

		file.save(path)


		# newImagePath = os.path.join(UPLOAD_IMAGES, file.filename)
		newImagePath = ""

		classResult = "test label"

		# # Sets the model if not already done and attempts to classify the image
		# setModel()
		# global model
		dest = os.path.join(ROOT_FOLDER,RESULT_IMAGES,file.filename)

		classResult = imageClassification.classifyImage(path,dest)

		# # Passes the image path to be processed and the destination directory path
		# destDir = app.config['STATIC_FOLDER']
		# newImagePath = ip.processImage(path,destDir)
		newImagePath = os.path.join(RESULT_IMAGES,file.filename)

		# Renders upload page with classification info and the processed image
		return render_template('upload.html',valid_submit = True, display_image = newImagePath, class_label = classResult)

		return render_template('upload.html',valid_submit = False)

