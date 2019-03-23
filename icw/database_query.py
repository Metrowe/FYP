# Custom database imports
import database_classes as table
from database_connection import Session

### START USER QUERIES ###
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
def filterGalleryImages(category,label):
	partialQuery = Session.query(table.Image)\
	.join(table.Image,table.Submission.images)\
	.filter(table.Submission.modApproval==True)

	if label != None:
		partialQuery = partialQuery.filter(table.Submission.animalLabel==label)

	if category != None:
		partialQuery = partialQuery.filter(table.Image.type==category)

	images = partialQuery.all()

	return images

def filterMyuploadsImages(category,label,id):
	partialQuery = Session.query(table.Image)\
	.join(table.Image,table.Submission.images)\
	.filter(table.Submission.userId==id)

	if label != None:
		partialQuery = partialQuery.filter(table.Submission.animalLabel==label)

	if category != None:
		partialQuery = partialQuery.filter(table.Image.type==category)

	images = partialQuery.all()

	return images
### END IMAGE QUERIES ###

### START ADMIN QUERIES ###
def idSubmission(id):
	submission = Session.query(table.Submission).\
	filter(table.Submission.id==id).first()

	return submission
### END IMAGE QUERIES ###

### START ADMIN QUERIES ###
def reviewSubmissions():
	submissions = Session.query(table.Submission)\
	.filter(table.Submission.permissionGallery==True)\
	.filter(table.Submission.modReviewed==False).all() 

	return submissions

def allUsers():
	users = Session.query(table.User).all() 
	
	return users

def allSubmissions():
	submissions = Session.query(table.Submission).all() 
	return submissions

def allImages():
	images = Session.query(table.Image).all() 
	return images

def allFeedbacks():
	feedbacks = Session.query(table.Feedback).all()
	return feedbacks
### END ADMIN QUERIES ###