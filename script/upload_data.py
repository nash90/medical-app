# coding=utf-8

import os
import json
import pandas as pd

from base import Base
from base import engine
from config import settings

# set constants colomn names in excel
Drug_Class = "Drug_Class"
Drug_SubClass = "Drug_SubClass"
Drug_Name = "Drug_Name"
BB_Warning = "BB_Warning"
Drug_Information_Type = "Drug_Information_Type"
Drug_Information = "Drug_Information"
Scrabble_Hint = "Scrabble_Hint"
Keyword = "Keyword"


file = settings['file_src']
drug_info_sheet_name = settings['drug_info_sheet_name']

df_drug_info = pd.read_excel(file, sheetname=drug_info_sheet_name)
#print(df_drug_info)

def createTableIfNotExit():
  Base.metadata.create_all(engine)

def updateDrugClass(row):
  drug_class = row["Drug_Class"]

def run_script():
  #createTableIfNotExit()
  for index, row in df_drug_info.iterrows():
    updateDrugClass() 
#session = Session()

#session.commit()
#session.close()