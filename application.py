import os
from flask import Flask, render_template, request, render_template_string

# EB looks for an 'application' callable by default.
# application = Flask(__name__,root_path='app_files')
application = Flask(__name__,template_folder="app_files/templates",static_folder="app_files/static")

APP_ROOT = os.path.basename('app_files')
# APP_TEMPLATES = os.path.join(APP_ROOT,'templates')
# application.config['TEMPLATES_FOLDER'] = TEMPLATES_FOLDER

STATIC_FOLDER = os.path.basename('static')

EXAMPLE_IMAGES = os.path.join(STATIC_FOLDER,'images','examples')
RESULT_IMAGES = os.path.join(STATIC_FOLDER,'images','results')
UPLOAD_IMAGES = os.path.join(STATIC_FOLDER,'images','uploads')
# STATIC_FOLDER = os.path.join(APP_ROOT,'static')
# application.config['STATIC_FOLDER'] = STATIC_FOLDER


@application.route('/')
def index():
	# print(application.config)
	# listOfFiles = os.listdir('.') 
	print(STATIC_FOLDER)
	# print(APP_TEMPLATES)

	return str(os.listdir('app_files/static/images/examples')) + " --- " + str(os.listdir('.')) 
	# return str(os.listdir('/app_files/static/images/examples/.')) + " XXXX " + str(os.listdir('/static/images/examples/.'))

	# return render_template("index.html",exampleImage = os.path.join(EXAMPLE_IMAGES,'deereg.jpg'))
    

    # return "name change"
    # print(application.config)

@application.route('/upload')
def upload():
    return render_template('upload.html')

# run the application.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    application.debug = True
    application.run()