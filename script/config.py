import os

url = os.environ['PSQL_DB_HOST'] + ':5432/' + os.environ['PSQL_DB_NAME']
settings = {
  "db_type":"postgresql",
  "db_url": url,
  "db_username": os.environ['PSQL_DB_USER'],
  "db_password": os.environ['PSQL_DB_PWD'],
  "file_src":"./data/Cardio and Mental Drug Game.xlsx",
  "drug_info_sheet_name":"Project",
  "quiz_sheet_name":"Drug Quiz Question",
  "quiz_option_sheet_name":"Drug Quiz Option",
  "db_debug_flag":False
}
