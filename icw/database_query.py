# import json
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Integer, String, Boolean, Text
# from sqlalchemy import Column, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import func

# Custom database imports
import database_classes as table
from database_connection import Session

### START USER QUERIES ###
def allUsers():
	users = Session.query(table.User).all() 
	
	return users

def namePassUser(username,password):
	user = Session.query(table.User)\
	.filter(table.User.username==username)\
	.filter(table.User.password==password).first()

	return user

def nameUser(username):
	user = Session.query(table.User)\
	.filter(table.User.username==username).first()

	return user

def idUserExist(id):
	user = Session.query(table.User)\
	.filter(table.User.id==id).first()

	return user != None

def idUserAdmin(id):
	user = Session.query(table.User)\
	.filter(table.User.id==id)\
	.filter(table.User.admin==True).first()

	return user != None
### END USER QUERIES ###

### START IMAGE QUERIES ###
def allImages():
	images = Session.query(table.Image).all() 

	return images

def allGalleryImages():
	images = list( Session.query(table.Image).join(table.Image,table.Submission.originalImage).filter(table.Submission.modApproval==True) )

	return images

def filterGalleryImages(original,isolate,label):
	images = []

	if label != None:
		if original:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.originalImage)\
				.filter(table.Submission.modApproval==True)\
				.filter(table.Submission.animalLabel==label)
			)

		if isolate:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.isolateImage)\
				.filter(table.Submission.modApproval==True)\
				.filter(table.Submission.animalLabel==label)
			)
	else:
		if original:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.originalImage)\
				.filter(table.Submission.modApproval==True)
			)

		if isolate:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.isolateImage)\
				.filter(table.Submission.modApproval==True)
			)

	return images

def filterMyuploadsImages(original,isolate,label,id):
	images = []

	if label != None:
		if original:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.originalImage)\
				.filter(table.Submission.userId==id)\
				.filter(table.Submission.animalLabel==label)
			)

		if isolate:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.isolateImage)\
				.filter(table.Submission.userId==id)\
				.filter(table.Submission.animalLabel==label)
			)
	else:
		if original:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.originalImage)\
				.filter(table.Submission.userId==id)
			)

		if isolate:
			images = images + list( \
				Session.query(table.Image)\
				.join(table.Image,table.Submission.isolateImage)\
				.filter(table.Submission.userId==id)
			)

	return images
### END IMAGE QUERIES ###

### START SUBMISSION QUERIES ###
def reviewSubmissions():
	submissions = Session.query(table.Submission)\
	.filter(table.Submission.userPermission==True)\
	.filter(table.Submission.modReviewed==False).all() 

	return submissions

def allSubmissions():
	submissions = Session.query(table.Submission).all() 

	return submissions

def idSubmission(id):
	submission = Session.query(table.Submission).\
	filter(table.Submission.id==id).first()

	return submission
