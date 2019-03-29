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

	return success
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

def insertGuestSubmission(originalPath,isolatePath,summaryPath,animalLabel,permissionGallery,permissionDataset):
	newSubmission = table.Submission(animalLabel=animalLabel,firstLabel=animalLabel, permissionGallery=permissionGallery, permissionDataset=permissionDataset, modApproval=False, modReviewed=False)

	newSubmission.images.append(table.Image(type='original',path=originalPath))
	newSubmission.images.append(table.Image(type='isolate',path=isolatePath))
	newSubmission.images.append(table.Image(type='summary',path=summaryPath))

	Session.add(newSubmission)
	success = safeCommit()

	newSubmissionId = None
	if success:
		newSubmissionId = newSubmission.id

	return newSubmissionId

def insertUserSubmission(originalPath,isolatePath,summaryPath,animalLabel,permissionGallery,permissionDataset,userId):
	newSubmission = table.Submission(animalLabel=animalLabel, firstLabel=animalLabel, permissionGallery=permissionGallery, permissionDataset=permissionDataset, modApproval=False, modReviewed=False,userId=userId)

	newSubmission.images.append(table.Image(type='original',path=originalPath))
	newSubmission.images.append(table.Image(type='isolate',path=isolatePath))
	newSubmission.images.append(table.Image(type='summary',path=summaryPath))

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
		submission.feedback = table.Feedback(rateClassify=rateClassify,rateIsolate=rateIsolate,commentResult=commentResult,commentSite=commentSite)

		Session.add(submission)
		success = safeCommit()

		if not success:
			submission = None

	return submission

def updateModApproval(submissionId,approval,labelUpdate):
	submission = dbQuery.idSubmission(submissionId)

	if submission != None:
		submission.modApproval = approval
		submission.modReviewed = True

		if labelUpdate != None:
			submission.animalLabel = labelUpdate

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
		for image in submission.images:
			print('image.path',image.path)
			fileManagement.deleteFile(image.path)
			Session.delete(image)

		Session.delete(submission)
		success = safeCommit()
	else:
		success = False

	return success
### END DELETES ###