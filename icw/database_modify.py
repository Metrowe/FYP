# from sqlalchemy import Integer, String, Boolean, Text
# from sqlalchemy import Column, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import func

# Custom database imports
from database_connection import Session
import database_classes as table
import database_query as dbQuery

# Generic imports
import os_fileManagement as fileManagement

### START ERROR PREVENTION ###
def safeCommit():
	success = False
	try:
		Session.commit()
		success = True
	except Exception as e:
		print('Exception:', e)
		Session.rollback()
		Session.flush()
		success = False
### END ERROR PREVENTION ###

### START INSERTS ###
def insertUser(username,password):
	newUser = None
	existingUser = dbQuery.nameUser(username)

	if existingUser == None:
		newUser = table.User(username=username,password=password,admin=False)
		Session.add(newUser)
		success = safeCommit()

		if not success:
			newUser = None

	return newUser

def insertAdmin(username,password):
	newUser = None
	existingUser = dbQuery.nameUser(username)

	if existingUser == None:
		newUser = table.User(username=username,password=password,admin=True)
		Session.add(newUser)
		safeCommit()
	else:
		newUser = None

	return newUser

def insertGuestSubmission(originalPath,isolatePath,classResult,userPermission):
	newSubmission = table.Submission(userPermission=userPermission, modApproval=False, modReviewed=False, animalLabel=classResult)
	newSubmission.originalImage = table.Image(path=originalPath,original=True)
	newSubmission.isolateImage = table.Image(path=isolatePath,original=False)

	Session.add(newSubmission)
	success = safeCommit()

	newSubmissionId = None
	if success:
		newSubmissionId = newSubmission.id

	return newSubmissionId

def insertUserSubmission(originalPath,isolatePath,classResult,userId,userPermission):
	newSubmission = table.Submission(userPermission=userPermission, modApproval=False, modReviewed=False, animalLabel=classResult,userId=userId)
	newSubmission.originalImage = table.Image(path=originalPath,original=True)
	newSubmission.isolateImage = table.Image(path=isolatePath,original=False)

	Session.add(newSubmission)
	success = safeCommit()

	newSubmissionId = None
	if success:
		newSubmissionId = newSubmission.id

	return newSubmissionId
### END INSERTS ###

### START UPDATES ###
def updateFeedback(submissionId,rateClassify,rateIsolate,commentResult,commentSite):
	submission = dbQuery.idSubmission(submissionId)

	if submission != None:
		submission.subFeedback = table.Feedback(rateClassify=rateClassify,rateIsolate=rateIsolate,commentResult=commentResult,commentSite=commentSite)

		Session.add(submission)
		success = safeCommit()

		if not success:
			submission = None

	return submission

def updateModApproval(submissionId,approval):
	submission = dbQuery.idSubmission(submissionId)

	if submission != None:
		submission.modApproval = approval
		submission.modReviewed = True

		Session.add(submission)
		success = safeCommit()

		if not success:
			submission = None

	return submission
### END UPDATES ###

### START DELETES ###
def deleteSubmission(submissionId):
	submission = dbQuery.idSubmission(submissionId)

	if submission != None:
		if submission.originalImage != None:
			fileManagement.deleteFile(submission.originalImage.path)
			Session.delete(submission.originalImage)
		if submission.isolateImage != None:
			fileManagement.deleteFile(submission.isolateImage.path)
			Session.delete(submission.isolateImage)
		if submission.subFeedback != None:
			Session.delete(submission.subFeedback)

		Session.delete(submission)
		success = safeCommit()
	else:
		success = False

	return success
### END DELETES ###