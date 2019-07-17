# coding=utf-8

from sqlalchemy import Column, String, Boolean, Numeric, Integer, Date, Table, ForeignKey, DateTime, Sequence
from base import Base

class DrugClass(Base):
  __tablename__ = 'drug_class'
  drug_class_id = Column('drug_class_id', Integer, primary_key=True)
  drug_class_name = Column('drug_class_name', String(32))
  drug_class_description = Column('drug_class_description', String(32))

class DrugSubClass(Base):
  __tablename__ = 'drug_subclass'
  drug_subclass_id = Column('drug_subclass_id', Integer, primary_key=True)
  drug_class_id = Column('drug_class_id', Integer, ForeignKey('drug_class.drug_class_id'))
  drug_subclass_name = Column('drug_subclass_name', String(32))
  drug_subclass_description = Column('drug_class_description', String(32))

class Drug(Base):
  __tablename__ = 'drug'
  drug_id = Column('drug_id', Integer, primary_key=True)
  drug_subclass_id = Column('drug_subclass_id', Integer, ForeignKey('drug_subclass.drug_subclass_id'))
  drug_name = Column('drug_name', String(32))
  black_box_warning = Column('black_box_warning', String(500))

class DrugInformationType(Base):
  __tablename__ = 'drug_information_type'
  drug_info_type_id = Column('drug_info_type_id', Integer, primary_key=True)
  drug_information_type = Column('drug_information_type', String(32))
  game_level = Column('game_level', Integer)

class DrugInformation(Base):
  __tablename__ = 'drug_information'
  drug_info_id = Column('drug_info_id', Integer, primary_key=True)
  drug_id = Column('drug_id', Integer, ForeignKey('drug.drug_id'))
  drug_info_type_id = Column('drug_info_type_id', Integer, ForeignKey('drug_information_type.drug_info_type_id'))
  information = Column('information', String(1024))
  scrabble_hint = Column('scrabble_hint', String(1024))

class DrugKeyword(Base):
  __tablename__ = 'drug_keyword'
  keyword_id = Column('keyword_id', Integer, primary_key=True)
  drug_info_id = Column('drug_info_id', Integer, ForeignKey('drug_information.drug_info_id'))
  keyword = Column('keyword', String(32))

class DrugQuizQuestion(Base):
  __tablename__ = 'drug_quiz_question'
  drug_quiz_id = Column('drug_quiz_id', Integer, primary_key=True)
  drug_id = Column('drug_id', Integer, ForeignKey('drug.drug_id'))
  drug_info_type_id = Column('drug_info_type_id', Integer, ForeignKey('drug_information_type.drug_info_type_id'))
  quiz_question = Column('quiz_question', String(500))
  enable = Column('enable', Boolean)

class DrugQuizOption(Base):
  __tablename__ = 'drug_quiz_option'
  quiz_option_id = Column('quiz_option_id', Integer, primary_key=True)
  quiz_id = Column('quiz_id', Integer, ForeignKey('drug_quiz_question.drug_quiz_id'))
  quiz_option = Column('quiz_option', String(200))
  correct_flag = Column('correct_flag', Boolean)

