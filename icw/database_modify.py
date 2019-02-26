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


# max_id = session.query(func.max(Table.column)).scalar()

###################################################
# Session = sessionmaker(bind=engine)

# session = Session()

# tempUser = table.User(id=1, username='temp', password='secure')
# session.add(tempUser)
# our_user = session.query(table.User).first() 
# print(type(our_user))
# print(our_user.id)
# print(our_user is tempUser)

def insertGuestSubmission(originalPath,isolatePath,classResult):
	#need to find a way of managing ids
	nextSubmissionId = 1
	newSubmission = table.Submission(id=nextSubmissionId, galleryPass=True, modApproval=False, animalLabel=classResult)
	
	# TODO: fix id issue
	nextImageId = 1
	newSubmission.originalId = nextImageId
	newSubmission.originalImage = table.Image(id=nextImageId, path=originalPath,original=True)

	# TODO: fix id issue
	nextImageId = 2
	newSubmission.isolateId = nextImageId
	newSubmission.isolateImage = table.Image(id=nextImageId, path=isolatePath,original=False)


	Session.add(newSubmission)

	our_result = Session.query(table.Image).first() 
	print('Animal label: ' + str(our_result.submission.animalLabel))

	return True
#####################################################