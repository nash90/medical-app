# coding=utf-8

import os
import json
import pandas as pd
import math
import logging

from base import Base
from base import engine
from base import Session
from config import settings

from models import DrugClass
from models import DrugSubClass

# set constants colomn names in excel
Drug_Class = "Drug_Class"
Drug_SubClass = "Drug_SubClass"
Drug_Name = "Drug_Name"
BB_Warning = "BB_Warning"
Drug_Information_Type = "Drug_Information_Type"
Drug_Information = "Drug_Information"
Scrabble_Hint = "Scrabble_Hint"
Keyword = "Keyword"
Quiz_Question = "Quiz_Question"
Quiz_Type = "Quiz_Type"
Enable = "Enable"

file = settings['file_src']
drug_info_sheet_name = settings['drug_info_sheet_name']

df_drug_info = pd.read_excel(file, sheet_name=drug_info_sheet_name)
#print(df_drug_info)

def createTableIfNotExit():
  Base.metadata.create_all(engine)

def isNan(value):
  if type(value) == float:
    return math.isnan(value)
  return False

def getIDFromName(name, model):
  if isNan(name) == False and model == 'DrugClass':
    has_item = session.query(DrugClass).filter(DrugClass.drug_class_name == name).all()
    if len(has_item) > 0:
      item = has_item[0]
      return item.drug_class_id
    else:
      return None
  return None

def updateDrugClass(row):
  drug_class = row[Drug_Class]
  if isNan(drug_class) == False:
    has_class = session.query(DrugClass).filter(DrugClass.drug_class_name == drug_class).all()
    if len(has_class) < 1:
      new_drug_class = DrugClass(drug_class_name=drug_class)
      session.add(new_drug_class)

def updateDrugSubClass(row):
  drug_subclass_name = row[Drug_SubClass]
  drug_class = row[Drug_Class]
  drug_class_id = getIDFromName(drug_class, 'DrugClass')

  new_drugsub_class = DrugSubClass(drug_class_id=drug_class_id, drug_subclass_name=drug_subclass_name)
  
  if isNan(drug_subclass_name) == False:
    has_item = session.query(DrugSubClass).filter(DrugSubClass.drug_subclass_name == drug_subclass_name).all()
    if len(has_item) < 1:
      session.add(new_drugsub_class)
    else:
      for item in has_item:
        item.drug_subclass_name = new_drugsub_class.drug_subclass_name
        item.drug_class_id = new_drugsub_class.drug_class_id


def run_script():
  for index, row in df_drug_info.iterrows():
    if index>1:
      break
    updateDrugClass(row) 
    updateDrugSubClass(row)

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
session = Session()
createTableIfNotExit()
run_script()
session.commit()
session.close()