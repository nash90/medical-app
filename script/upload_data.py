# coding=utf-8

import os
import json
import pandas as pd
import math
import logging
import traceback

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
Keyword2 = "Keyword2"
Keyword3 = "Keyword3"
Keyword4 = "Keyword4"
Keyword5 = "Keyword5"
Quiz_Question = "Quiz_Question"
Quiz_Type = "Quiz_Type"
Drug_Quiz_Id = "Drug_Quiz_Id"
Drug_Option = "Drug_Option"
Correct_Answer_Flag = "Correct_Answer_Flag"
Drug_Quiz_Option = "Drug_Quiz_Option"
Enable = "Enable"

file = settings['file_src']
drug_info_sheet_name = settings['drug_info_sheet_name']
quiz_sheet_name = settings['quiz_sheet_name']
quiz_option_sheet_name = settings['quiz_option_sheet_name']
db_debug_flag = settings['db_debug_flag']

df_drug_info = pd.read_excel(file, sheet_name=drug_info_sheet_name)
df_quiz = pd.read_excel(file, sheet_name=quiz_sheet_name)
df_quiz_opt = pd.read_excel(file, sheet_name=quiz_option_sheet_name)
#print(df_drug_info)

def createTableIfNotExit():
  return Base.metadata.create_all(engine)

def dropAllTable():
  return Base.metadata.drop_all(engine)

def dropQuizTables():
  DrugQuizOption.__table__.drop(engine)
  DrugQuizQuestion.__table__.drop(engine)

def addDataToDB(obj):
  session.add(obj)
  try:  
    session.commit()
  except Exception as e:
    session.rollback()
    #print(e)
    raise e
    

def isNan(value):
  if type(value) == float:
    return math.isnan(value)
  elif value == "" or value == None:
    return True
  return False

def strip(value):
  if type(value) == str:
    return value.strip()
  else:
    return value

def getModelNameAttribute(model):
  if model == DrugClass:
    return {"attribute":DrugClass.drug_class_name,"id":"drug_class_id"}
  elif model == DrugSubClass:
    return {"attribute":DrugSubClass.drug_subclass_name, "id":"drug_subclass_id"}
  elif model == Drug:
    return {"attribute":Drug.drug_name, "id":"drug_id"}
  elif model == DrugInformationType:
    return {"attribute":DrugInformationType.drug_information_type, "id":"drug_info_type_id"}
  elif model == DrugKeyword:
    return {"attribute":DrugKeyword.keyword, "id":"keyword_id"}    

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

def updateDrugClass(row):
  drug_class = strip(row[Drug_Class])
  if isNan(drug_class) == False:
    has_item = session.query(DrugClass).filter(DrugClass.drug_class_name == drug_class).all()
    if len(has_item) < 1:
      new_item = DrugClass(drug_class_name=drug_class)
      session.add(new_item)

def updateDrugInformationType(row):
  drug_information_type = strip(row[Drug_Information_Type])
  
  if isNan(drug_information_type) == False:
    new_item = DrugInformationType(drug_information_type=drug_information_type)
    has_item = session.query(DrugInformationType).filter(DrugInformationType.drug_information_type == drug_information_type).all()
    if len(has_item) < 1:
      session.add(new_item)

def updateDrugSubClass(row):
  drug_subclass_name = strip(row[Drug_SubClass])
  drug_class = strip(row[Drug_Class])
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
  drug_subclass_name = strip(row[Drug_SubClass])
  drug_subclass_id = getIDFromDB(drug_subclass_name, DrugSubClass)
  #print("debug", drug_subclass_id)
  drug_name = strip(row[Drug_Name])
  black_box_warning = strip(row[BB_Warning])

  new_item = Drug(drug_subclass_id=drug_subclass_id, drug_name = drug_name, black_box_warning=black_box_warning)

  if isNan(drug_name) == False:
    has_item = session.query(Drug).filter(getModelNameAttribute(Drug)["attribute"]== drug_name).all()
    if len(has_item) < 1:
      session.add(new_item)
    else:
      for item in has_item:
        update_attr = ["drug_subclass_id","drug_name","black_box_warning"]
        item = updatePersistingObject(item,new_item,update_attr)


def getKeywordBackup(row):
  keywords = [row[Keyword], row[Keyword2], row[Keyword3], row[Keyword4], row[Keyword5]]
  keywords = list(filter(lambda x: (isNan(x) == False), keywords))
  return "; ".join(keywords)
  

def updateDrugInformation(row):
  drug_name = strip(row[Drug_Name])
  drug_id = getIDFromDB(drug_name, Drug)
  drug_information_type = strip(row[Drug_Information_Type])
  drug_info_type_id = getIDFromDB(drug_information_type, DrugInformationType)
  information = strip(row[Drug_Information])
  scrabble_hint = strip(row[Scrabble_Hint])
  keyword_bk = getKeywordBackup(row)

  new_item = DrugInformation(drug_id=drug_id, drug_info_type_id=drug_info_type_id, 
  information=information, scrabble_hint=scrabble_hint, keyword_bk = keyword_bk)

  if isNan(information) == False:
    session.add(new_item)
  else:
    print("Could not insert Information: " + str(drug_name) + str(drug_information_type) + str(information))
  

def updateDrugKeyword(row):
  drug_name = strip(row[Drug_Name])
  drug_info_type = strip(row[Drug_Information_Type])
  drug_information = strip(row[Drug_Information])
  #drug_keyword = row[Keyword]
  keyword, keyword2, keyword3, keyword4, keyword5 = strip(row[Keyword]), strip(row[Keyword2]), strip(row[Keyword3]), strip(row[Keyword4]), strip(row[Keyword5])

  if isNan(drug_name) == False and isNan(drug_info_type) == False and isNan(drug_information) == False and isNan(keyword) == False:
    drug_information_obj = session.query(DrugInformation).join(
      Drug).join(
      DrugInformationType).filter(
      Drug.drug_name == drug_name).filter(
      DrugInformationType.drug_information_type == drug_info_type).filter(
      DrugInformation.information == drug_information).all()

    drug_info = drug_information_obj[0]

    #keywords = [x.strip() for x in drug_keyword.split(";")]
    keywords =[keyword,keyword2,keyword3,keyword4, keyword5]
    keywords = list(filter(lambda x:(type(x)==str),keywords))
    keywords = list(filter(None,keywords))

    for keyword in keywords:
      keyword_obj = None
      keyword_id = getIDFromDB(keyword, DrugKeyword)
      if  keyword_id == None:
        keyword_obj = DrugKeyword(keyword=keyword)
      else:
        keyword_obj = session.query(DrugKeyword).get(keyword_id)
      if keyword_obj != None:
        drug_info.keyword.append(keyword_obj)  
  
def updateQuizQuestion(row):
  drug_quiz_id = int(row[Drug_Quiz_Id])
  drug_name = strip(row[Drug_Name])
  drug_information_type = strip(row[Drug_Information_Type])
  quiz_question = strip(row[Quiz_Question])
  quiz_type = strip(row[Quiz_Type])

  if isNan(drug_name) == False and isNan(drug_information_type) == False and isNan(quiz_question) == False and isNan(quiz_type) == False:
    drug_name = drug_name.lower()
    
    drug = session.query(Drug).filter(
      Drug.drug_name == drug_name
    ).all()
    #print(drug)
    if len(drug) == 0:
      raise Exception('Could not find Drug :'+drug_name)
    drug = drug[0]

    drug_information = session.query(DrugInformationType).filter(
      DrugInformationType.drug_information_type == drug_information_type
    ).all()[0]

    drug_id = drug.drug_id
    drug_info_type_id = drug_information.drug_info_type_id


    new_item = DrugQuizQuestion(drug_quiz_id = drug_quiz_id, drug_id=drug_id, drug_info_type_id=drug_info_type_id, quiz_question=quiz_question,
    quiz_type=quiz_type)
    addDataToDB(new_item)

def updateQuizOption(row):
  quiz_id = row[Drug_Quiz_Id]
  drug_quiz_option = row[Drug_Quiz_Option]
  correct_answer = row[Correct_Answer_Flag]
  correct_answer_flag = True if type(correct_answer) == str and correct_answer.lower() == "correct" else False

  if isNan(quiz_id) == False and isNan(drug_quiz_option) == False and isNan(correct_answer_flag) == False:
    new_item = DrugQuizOption(quiz_id=quiz_id, quiz_option=drug_quiz_option, correct_flag=correct_answer_flag)
    addDataToDB(new_item)

def uploadDrugInfoData():
  for index, row in df_drug_info.iterrows():
    if index>900:
      break  
    updateDrugClass(row) 
    updateDrugSubClass(row)
    updateDrugInformationType(row)
    updateDrug(row)
    updateDrugInformation(row)
    updateDrugKeyword(row)
  session.commit()
  print("Processed Drug Information sheet")

def uploadQuizQuestion():
  for index, row in df_quiz.iterrows():
    try:
      updateQuizQuestion(row)
    except Exception as e:
      print(e)
      #print(traceback.format_exc())
  print("Processed Drug Question sheet")

def uploadQuizOption():
  for index, row in df_quiz_opt.iterrows():
    try:
      updateQuizOption(row)
    except Exception as e:
      print(str(type(e)) + ": Failed to upload quiz option :", str(row[Drug_Quiz_Id]) + " - " +row[Drug_Quiz_Option])
  print("Processed Drug Quiz Option sheet")

def run_script():
  print("Script Started ...")
  dropAllTable() 
  #dropQuizTables() # for debuging
  createTableIfNotExit()
  uploadDrugInfoData()
  uploadQuizQuestion()
  uploadQuizOption()
  session.close()
  print("Script Completed ...")

if db_debug_flag == True:
  logging.basicConfig()
  logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

session = Session()
run_script()
#session.close()

  



