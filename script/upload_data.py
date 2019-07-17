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
from models import DrugInformation
from models import DrugKeyword
from models import Drug
from models import DrugInformationType
from models import DrugQuizQuestion
from models import DrugQuizOption


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
  elif value == "" or value == None:
    return True
  return False

def getModelNameAttribute(model):
  if model == DrugClass:
    return {"attribute":DrugClass.drug_class_name,"id":"drug_class_id"}
  elif model == DrugSubClass:
    return {"attribute":DrugSubClass.drug_subclass_name, "id":"drug_subclass_id"}
  elif model == Drug:
    return {"attribute":Drug.drug_name, "id":""}
  elif model == DrugInformationType:
    return {"attribute":DrugInformationType.drug_information_type, "id":""}

def updatePersistingObject(persisted, new, attr):
  for item in attr:
    setattr(persisted, item, getattr(new,item))
  return persisted

def getIDFromDB(name, model):
  try:
    attribute = getModelNameAttribute(model)["attribute"]
    model_id_key =  getModelNameAttribute(model)["id"]
    if isNan(name) == False:
      has_item = session.query(model).filter(attribute == name).all()
      if len(has_item) > 0:
        item = has_item[0]
        return getattr(item, model_id_key)
      else:
        return None
  except Exception as e:
    print("cant get id from db",e)

def getIDFromName(name, model):
  if isNan(name) == False and model == 'DrugClass':
    has_item = session.query(DrugClass).filter(Drug_Class.drug_class_name == name).all()
    if len(has_item) > 0:
      item = has_item[0]
      return item.drug_class_id
    else:
      return None

  if isNan(name) == False and model == 'DrugSubClass':
    has_item = session.query(DrugSubClass).filter(DrugSubClass.drug_subclass_name == name).all()
    if len(has_item) > 0:
      item = has_item[0]
      return item.drug_subclass_id
    else:
      return None

  if isNan(name) == False and model == 'Drug':
    has_item = session.query(Drug).filter(Drug.drug_subclass_name == name).all()
    if len(has_item) > 0:
      item = has_item[0]
      return item.drug_subclass_id
    else:
      return None    

  return None

def updateDrugClass(row):
  drug_class = row[Drug_Class]
  if isNan(drug_class) == False:
    has_item = session.query(DrugClass).filter(DrugClass.drug_class_name == drug_class).all()
    if len(has_item) < 1:
      new_item = DrugClass(drug_class_name=drug_class)
      session.add(new_item)

def updateDrugInformationType(row):
  drug_information_type = row[Drug_Information_Type]
  
  if isNan(drug_information_type) == False:
    new_item = DrugInformationType(drug_information_type=drug_information_type)
    has_item = session.query(DrugInformationType).filter(DrugInformationType.drug_information_type == drug_information_type).all()
    if len(has_item) < 1:
      session.add(new_item)

def updateDrugSubClass(row):
  drug_subclass_name = row[Drug_SubClass]
  drug_class = row[Drug_Class]
  drug_class_id = getIDFromDB(drug_class, DrugClass)

  new_item = DrugSubClass(drug_class_id=drug_class_id, drug_subclass_name=drug_subclass_name)
  
  if isNan(drug_subclass_name) == False:
    has_item = session.query(DrugSubClass).filter(DrugSubClass.drug_subclass_name == drug_subclass_name).all()
    if len(has_item) < 1:
      session.add(new_item)
    else:
      for item in has_item:
        item.drug_subclass_name = new_item.drug_subclass_name
        item.drug_class_id = new_item.drug_class_id

def updateDrug(row):
  drug_subclass_name = row[Drug_SubClass]
  drug_subclass_id = getIDFromDB(drug_subclass_name, DrugSubClass)
  #print("debug", drug_subclass_id)
  drug_name = row[Drug_Name]
  black_box_warning = row[BB_Warning]

  new_item = Drug(drug_subclass_id=drug_subclass_id, drug_name = drug_name, black_box_warning=black_box_warning)

  if isNan(drug_name) == False:
    has_item = session.query(Drug).filter(getModelNameAttribute(Drug)["attribute"]== drug_name).all()
    if len(has_item) < 1:
      session.add(new_item)
    else:
      for item in has_item:
        update_attr = ["drug_subclass_id","drug_name","black_box_warning"]
        item = updatePersistingObject(item,new_item,update_attr)



def updateDrugInformation(row):
  drug_name = row[Drug_Name]
  drug_id = getIDFromDB(drug_name, Drug)
  drug_subclass_name = row[Drug_SubClass]
  drug_subclass_id = getIDFromDB(drug_subclass_name, DrugSubClass)

def run_script():
  for index, row in df_drug_info.iterrows():
    if index>5:
      break
    updateDrugClass(row) 
    updateDrugSubClass(row)
    updateDrugInformationType(row)
    updateDrug(row)
    #updateDrugInformation(row)

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
session = Session()
createTableIfNotExit()
run_script()
session.commit()
session.close()