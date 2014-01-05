import web

from sqlalchemy import create_engine, engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, TIMESTAMP, TEXT
from sqlalchemy.sql import text

system = create_engine('sqlite:///data.db', echo=True)

metadata = MetaData(bind=system)

data = Table('data', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', TEXT()),
    Column('content', TEXT()),
    Column('timestamp', TIMESTAMP(), server_default=text('current_timestamp')),
)

metadata.create_all()

db = web.database(dbn='sqlite', db='data.db')
