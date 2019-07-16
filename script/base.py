# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

url = settings["db_url"]
db_type = settings["db_type"]
username = settings["db_username"]
password = settings["db_password"]
engine = create_engine(db_type+'://'+username+':'+password + '@'+ url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
