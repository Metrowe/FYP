
# A very simple Flask Hello World app for you to get started with...
import time
import tensorflow
import cv2
import os
from flask import Flask, render_template, request, render_template_string

app = Flask(__name__,template_folder="app_files/templates",static_folder="app_files/static")

STATIC_FOLDER = os.path.basename('static')

EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','results')
UPLOAD_IMAGES = os.path.join(STATIC_FOLDER,'images','uploads')

@app.route('/')
def index():
    local_time = "Local time:" + time.ctime(time.time())

    # return local_time
    return render_template("index.html",exampleImage = os.path.join(EXAMPLE_IMAGES,'deereg.jpg'))
    # return render_template("index.html")

@application.route('/upload')
def upload():
    return render_template('upload.html')
