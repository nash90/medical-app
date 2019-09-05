# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from config import settings

url = settings["db_url"]
db_type = settings["db_type"]
username = settings["db_username"]
password = settings["db_password"]
full_url = db_type+'://'+username+':'+password + '@'+ url
engine = create_engine(full_url)
if not database_exists(engine.url):
    create_database(engine.url)
#engine = create_engine(full_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
