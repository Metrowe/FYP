from sqlalchemy.orm import sessionmaker


# from sqlalchemy import Integer, String, text, Boolean
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import database_classes as tables

# 'mysql+pymysql://' (the dialect and driver).
# 'student:datacamp' (the username and password).
# '@courses.csrrinzqubik.us-east-1.rds.amazonaws.com:3306/' (the host and port).
# 'census' (the database name).

# engine = create_engine('mysql+pymysql://'+'student:datacamp'+'@courses.csrrinzqubik.us-east-1.rds.amazonaws.com:3306/'+'census')
# engine = create_engine('mysql+pymysql://'+'metrowe:navybottle'+'@127.0.0.1:3306/'+'icwdata')
Base = declarative_base()

# Print the table names
# print(engine.table_names())




### TABLES ###
class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    path = Column(Text,nullable=False)
    animal = Column(Text,nullable=False)
    original = Column(Boolean,nullable=False)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    rateClassify = Column(Text,nullable=False)
    rateIsolate = Column(Text,nullable=False)
    commentResult = Column(Text,nullable=True)
    commentSite = Column(Text,nullable=True)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(Text,nullable=False)
    password = Column(Text,nullable=False)

class Submission(Base):
	__tablename__ = "submission"

	id = Column(Integer, primary_key=True)
	galleryPass = Column(Boolean,nullable=False)
	modApproval = Column(Boolean,nullable=False)

	originalId = Column(Integer,ForeignKey('image.id'))
	isolateId = Column(Integer,ForeignKey('image.id'))
	feedbackId = Column(Integer,ForeignKey('feedback.id'),nullable=True)
	userId = Column(Integer,ForeignKey('user.id'),nullable=True)

	originalImage = relationship(Image, foreign_keys=[originalId])
	isolateImage = relationship(Image, foreign_keys=[isolateId])
	# subFeedback = relationship(Feedback, foreign_keys=[feedbackId])
	# subUser = relationship(User, foreign_keys=[userUsername])
	subFeedback = relationship(Feedback)
	subUser = relationship(User)
### END TABLES ###


engine = create_engine('mysql://'+'metrowe:navybottle'+'@127.0.0.1:3306/'+'icwdata')

Base.metadata.create_all(engine)

print(engine.table_names())
