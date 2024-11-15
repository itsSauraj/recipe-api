'''
This file is used to create the database engine and create the tables in the database.
'''

from sqlalchemy import create_engine
from modals import DBBaseModel

engine = create_engine("sqlite+pysqlite:///databse.db", echo=True)
DBBaseModel.metadata.create_all(engine)