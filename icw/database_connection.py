from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import database_classes as table

# 'mysql+pymysql://' (the dialect and driver).
# 'student:datacamp' (the username and password).
# '@courses.csrrinzqubik.us-east-1.rds.amazonaws.com:3306/' (the host and port).
# 'census' (the database name).

# engine = create_engine('mysql+pymysql://'+'student:datacamp'+'@courses.csrrinzqubik.us-east-1.rds.amazonaws.com:3306/'+'census')
# engine = create_engine('mysql+pymysql://'+'metrowe:navybottle'+'@127.0.0.1:3306/'+'icwdata')
engine = create_engine('mysql://'+'metrowe:navybottle'+'@127.0.0.1:3306/'+'icwdata')
Base = declarative_base()

# Print the table names
# print(engine.table_names())

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name



print(engine.table_names())
print(User)