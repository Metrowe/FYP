from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import configuration_strings as config

engine = create_engine(config.databaseConnection,pool_recycle=1)

Session = scoped_session(sessionmaker(bind=engine))