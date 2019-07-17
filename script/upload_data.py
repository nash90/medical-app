# coding=utf-8

import os
import json
import pandas as pd

from base import Base
from base import engine
from base import Session
from config import settings

from models import DrugClass

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

def updateDrugClass(row):
  drug_class = row[Drug_Class]
  if type(drug_class) == str:
    has_class = session.query(DrugClass).filter(DrugClass.drug_class_name == drug_class).all()
    if len(has_class) < 1:
      new_drug_class = DrugClass(drug_class_name=drug_class)
      session.add(new_drug_class)

def run_script():
  for index, row in df_drug_info.iterrows():
    updateDrugClass(row) 

session = Session()
createTableIfNotExit()
run_script()
session.commit()
session.close()