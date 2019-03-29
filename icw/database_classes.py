from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref

Base = declarative_base()

### TABLES ###
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(Text,nullable=False)
    password = Column(Text,nullable=False)
    admin = Column(Boolean,nullable=False)

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    rateClassify = Column(Text,nullable=False)
    rateIsolate = Column(Text,nullable=False)
    commentResult = Column(Text,nullable=True)
    commentSite = Column(Text,nullable=True)

class Submission(Base):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    animalLabel = Column(Text,nullable=False)
    firstLabel = Column(Text,nullable=False)
    permissionGallery = Column(Boolean,nullable=False)
    permissionDataset = Column(Boolean,nullable=False)
    modApproval = Column(Boolean,nullable=False)
    modReviewed = Column(Boolean,nullable=False)

    feedbackId = Column(Integer,ForeignKey('feedback.id'),nullable=True)
    userId = Column(Integer,ForeignKey('user.id'),nullable=True)

    feedback = relationship(Feedback, backref=backref("submission", uselist=False))
    user = relationship(User, backref="submission")

class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    type = Column(Text,nullable=False)
    path = Column(Text,nullable=False)
    
    submissionId = Column(Integer,ForeignKey('submission.id'))  

    submission = relationship(Submission, backref="images")
### END TABLES ###