import web
import time

"""
Database module
This module use the ORM SQLAlchemy
"""
from sqlalchemy import create_engine, engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, TEXT
from sqlalchemy.sql import text


# ORM Settings and Database connection
system = create_engine('sqlite:///data.db', echo=True)
metadata = MetaData(bind=system)

# Create table rows
data = Table('data', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', TEXT()),
    Column('content', TEXT()),
    Column('timestamp', TEXT()),
)

# Create table rows
data = Table('user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', TEXT()),
    Column('color', TEXT()),
    Column('timestamp', TEXT()),
)

metadata.create_all()

db = web.database(dbn='sqlite', db='data.db')
