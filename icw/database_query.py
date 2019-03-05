import json

from sqlalchemy.orm import sessionmaker

from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

import database_classes as table
from database_connection import Session

# import database_modify as dbModify




# print( dbModify.insertGuestSubmission('asdsasd','asdadsdas','animalresult maybe') )
def namePassUser(username,password):
	user = Session.query(table.User)\
	.filter(table.User.username==username).first()

	return user

def nameUser(username):
	user = Session.query(table.User)\
	.filter(table.User.username==username).first()

	return user

def allImages():
	images = Session.query(table.Image).all() 


	for i in images:
		print('imageId = ' + str(i.id))

	return images

def allSubmissions():
	submissions = Session.query(table.Submission).all() 
	
	for s in submissions:
		print('submissionId = ' + str(s.id))

	return submissions

def allUsers():
	users = Session.query(table.User).all() 
	
	for u in users:
		print('userid = ' + str(u.id) + ' username = ' + str(u.username))

	return users


#Rename
def allGalleryImages():
	#join can essentially be used as filter to submissions as only one will be associated


	# images = Session.query(table.Image).filter(table.Image.original==True).filter(table.Image.submission.id==1) 

	# images = Session.query(table.Image).filter(table.Image.original==True)

	# images = Session.query(table.Image).join(table.Image,table.Submission.originalImage).filter(table.Image.original==True).filter(table.Submission.modApproval==False)
	# images = Session.query(table.Image).join(table.Image,table.Submission.originalImage).filter(table.Image.original==True).filter(table.Submission.modApproval==True)


	# images = Session.query(table.Image).join(table.Image,table.Submission.originalImage).filter(table.Submission.modApproval==True)

	#This is the actual get all gallery images query
	# images = list( Session.query(table.Image).join(table.Image,table.Submission.originalImage).filter(table.Submission.modApproval==True) ) \
	# + list( Session.query(table.Image).join(table.Image,table.Submission.isolateImage).filter(table.Submission.modApproval==True) )

	images = list( Session.query(table.Image).join(table.Image,table.Submission.originalImage).filter(table.Submission.modApproval==True) )

	# images = list(images)

	# print( type(images))
	# query.join(Address, User.addresses)  

	# db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))
	
	# myList = []
	# for i in range(10):
 #    	myList.append(i)

 # 	result = {
	# 	"inputPath": originalPath,
	# 	"outputPath": isolatePath,
	# 	"label": classResult
	# }


	# print(imagePaths)

	for i in images:
		print('imageId = ' + str(i.id) + ', path = ' + str(i.path))
		# print('label = ' + str(i.submission.animalLabel))
	return images

# allGalleryImages()

# def maxImageId():
# 	return our_user = session.query(table.User).first() 

# max_id = session.query(func.max(Table.column)).scalar()

