from sqlalchemy.orm import sessionmaker

from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import scoped_session

import database_classes as table

import configuration_strings as config

engine = create_engine(config.databaseConnection)

Session = scoped_session(sessionmaker(bind=engine))























# print( dbModify.insertGuestSubmission('asdsasd','asdadsdas','animalresult maybe') )
# for tbl in reversed(Base.metadata.sorted_tables):
#     engine.execute(tbl.delete())

##################################################################
# Session = sessionmaker(bind=engine)

# session = Session()

# tempUser = table.User(id=1, username='temp', password='secure')
# session.add(tempUser)

# our_user = session.query(table.User).first() 
# print(type(our_user))
# print(our_user.id)
# print(our_user is tempUser)

#################################################################

# tempSubmission = table.Submission(id=1, galleryPass=True, modApproval=False, animalLabel='turtlenotreally')
# newImageId = 1
# tempSubmission.originalId = newImageId
# tempSubmission.originalImage = table.Image(id=newImageId, path='/static/etc',original=True)

# newImageId = 2
# tempSubmission.isolateId = newImageId
# tempSubmission.isolateImage = table.Image(id=newImageId, path='/appfiles/next',original=False)


# Session.add(tempSubmission)

# our_result = Session.query(table.Image).all() 
# print("a is b = " + str( our_result[0] is our_result[1]))
# print("a.sub is b.sub = " + str( our_result[0].submission is our_result[1].submission))
# print(our_result[0].submission.animalLabel)
# print(our_result[1].submission.animalLabel)