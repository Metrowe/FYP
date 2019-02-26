from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import backref
from sqlalchemy.orm import backref

Base = declarative_base()

### TABLES ###
class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    path = Column(Text,nullable=False)
    # animal = Column(Text,nullable=False)
    original = Column(Boolean,nullable=False)

    # should add error handling in getter or at locations where getter is called
    @property
    def submission(self):
        if self.original == True:
            return self.originalLinkSub
        else:
            return self.isolateLinkSub

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    rateClassify = Column(Text,nullable=False)
    rateIsolate = Column(Text,nullable=False)
    commentResult = Column(Text,nullable=True)
    commentSite = Column(Text,nullable=True)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(Text,nullable=False)
    password = Column(Text,nullable=False)

# class Submission(Base):
# 	__tablename__ = "submission"

# 	id = Column(Integer, primary_key=True)
# 	galleryPass = Column(Boolean,nullable=False)
# 	modApproval = Column(Boolean,nullable=False)

# 	originalId = Column(Integer,ForeignKey('image.id'))
# 	isolateId = Column(Integer,ForeignKey('image.id'))
# 	feedbackId = Column(Integer,ForeignKey('feedback.id'),nullable=True)
# 	userId = Column(Integer,ForeignKey('user.id'),nullable=True)

# 	originalImage = relationship(Image, foreign_keys=[originalId])
# 	isolateImage = relationship(Image, foreign_keys=[isolateId])
# 	# subFeedback = relationship(Feedback, foreign_keys=[feedbackId])
# 	# subUser = relationship(User, foreign_keys=[userUsername])
# 	subFeedback = relationship(Feedback)
# 	subUser = relationship(User)

class Submission(Base):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    galleryPass = Column(Boolean,nullable=False)
    modApproval = Column(Boolean,nullable=False)
    animalLabel = Column(Text,nullable=False)


    originalId = Column(Integer,ForeignKey('image.id'))
    isolateId = Column(Integer,ForeignKey('image.id'))
    feedbackId = Column(Integer,ForeignKey('feedback.id'),nullable=True)
    userId = Column(Integer,ForeignKey('user.id'),nullable=True)

    # Only one backref allowed ?needed?
    # Backref names very important as 
    originalImage = relationship(Image, foreign_keys=[originalId], backref=backref("originalLinkSub", uselist=False))
    isolateImage = relationship(Image, foreign_keys=[isolateId], backref=backref("isolateLinkSub", uselist=False))
    subFeedback = relationship(Feedback, backref=backref("submission", uselist=False))
    subUser = relationship(User, backref="submission")

    # originalImage = relationship(Image, foreign_keys=[originalId])
    # isolateImage = relationship(Image, foreign_keys=[isolateId])
    # subFeedback = relationship(Feedback)
    # subUser = relationship(User)

### END TABLES ###

# author = relationship("Author",backref="books")   
# child = relationship("Child", backref=backref("parent", uselist=False))