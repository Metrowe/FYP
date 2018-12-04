import os
from flask import Flask, render_template, request

import imageProcessing as ip
import imageClassification as ic

app = Flask(__name__)

# Sets config for uploads folder
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sets config for static folder
STATIC_FOLDER = os.path.basename('static')
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Global variable for storing the trained model
model = None

# Function for setting model if it is not already set
def setModel():
	global model
	if model == None:
		model = ic.getWeightedModel()

# Flask App index
# Renders a basic index page
@app.route('/')
def index():
    return render_template('index.html')

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
		path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		file.save(path)

		# Sets the model if not already done and attempts to classify the image
		setModel()
		global model
		classResult = ic.classifyImage(path,model)

		# Passes the image path to be processed and the destination directory path
		destDir = app.config['STATIC_FOLDER']
		newImagePath = ip.processImage(path,destDir)

		# Renders upload page with classification info and the processed image
		return render_template('upload.html',valid_submit = True, display_image = newImagePath, class_label = classResult)