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
# def allImages(session):
# 	return our_user = session.query(table.User).first() 

# def maxImageId():
# 	return our_user = session.query(table.User).first() 

# max_id = session.query(func.max(Table.column)).scalar()

