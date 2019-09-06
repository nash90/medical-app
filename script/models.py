# coding=utf-8

from sqlalchemy import Column, String, Boolean, Numeric, Integer, Date, Table, ForeignKey, DateTime, Sequence
from base import Base
from sqlalchemy.orm import relationship

class DrugClass(Base):
  __tablename__ = 'drug_class'
  drug_class_id = Column('drug_class_id', Integer, primary_key=True)
  drug_class_name = Column('drug_class_name', String(50))
  drug_class_description = Column('drug_class_description', String(200))

class DrugSubClass(Base):
  __tablename__ = 'drug_subclass'
  drug_subclass_id = Column('drug_subclass_id', Integer, primary_key=True)
  drug_class_id = Column('drug_class_id', Integer, ForeignKey('drug_class.drug_class_id'))
  drug_subclass_name = Column('drug_subclass_name', String(50))
  drug_subclass_description = Column('drug_subclass_description', String(200))

class Drug(Base):
  __tablename__ = 'drug'
  drug_id = Column('drug_id', Integer, primary_key=True)
  drug_subclass_id = Column('drug_subclass_id', Integer, ForeignKey('drug_subclass.drug_subclass_id'))
  drug_name = Column('drug_name', String(256))
  black_box_warning = Column('black_box_warning', String(500))
  drug_information = relationship("DrugInformation", back_populates="drug")
  drug_quiz_question = relationship("DrugQuizQuestion", back_populates="drug")

class DrugInformationType(Base):
  __tablename__ = 'drug_information_type'
  drug_info_type_id = Column('drug_info_type_id', Integer, primary_key=True)
  drug_information_type = Column('drug_information_type', String(50))
  game_level = Column('game_level', Integer)
  drug_information = relationship("DrugInformation", back_populates="drug_info_type")

keyword_association_table = Table('drug_info_keyword', Base.metadata,
  Column('relation_id', Integer, primary_key=True),
  Column('drug_info_id', Integer, ForeignKey('drug_information.drug_info_id')),
  Column('keyword_id', Integer, ForeignKey('drug_keyword.keyword_id'))
) 

class DrugInformation(Base):
  __tablename__ = 'drug_information'
  drug_info_id = Column('drug_info_id', Integer, primary_key=True)
  drug_id = Column('drug_id', Integer, ForeignKey('drug.drug_id'))
  drug_info_type_id = Column('drug_info_type_id', Integer, ForeignKey('drug_information_type.drug_info_type_id'))
  information = Column('information', String(1024))
  scrabble_hint = Column('scrabble_hint', String(1024))
  keyword_bk = Column('keyword_bk', String(1024))
  drug_info_type = relationship("DrugInformationType", back_populates="drug_information")
  drug = relationship("Drug", back_populates="drug_information")
  keyword = relationship("DrugKeyword",
                    secondary=keyword_association_table)

class DrugKeyword(Base):
  __tablename__ = 'drug_keyword'
  keyword_id = Column('keyword_id', Integer, primary_key=True)
  #drug_info_id = Column('drug_info_id', Integer, ForeignKey('drug_information.drug_info_id'))
  keyword = Column('keyword', String(256))


class DrugQuizQuestion(Base):
  __tablename__ = 'drug_quiz_question'
  drug_quiz_id = Column('drug_quiz_id', Integer, primary_key=True)
  drug_id = Column('drug_id', Integer, ForeignKey('drug.drug_id'))
  drug_info_type_id = Column('drug_info_type_id', Integer, ForeignKey('drug_information_type.drug_info_type_id'))
  quiz_question = Column('quiz_question', String(500))
  quiz_type = Column('quiz_type', String(200))
  enable = Column('enable', Boolean)
  drug = relationship("Drug", back_populates="drug_quiz_question")
  drug_quiz_option = relationship("DrugQuizOption", back_populates="drug_quiz_question")

class DrugQuizOption(Base):
  __tablename__ = 'drug_quiz_option'
  quiz_option_id = Column('quiz_option_id', Integer, primary_key=True)
  quiz_id = Column('quiz_id', Integer, ForeignKey('drug_quiz_question.drug_quiz_id'))
  quiz_option = Column('quiz_option', String(200))
  correct_flag = Column('correct_flag', Boolean)
  rational = Column('rational', String(500))
  drug_quiz_question = relationship("DrugQuizQuestion", back_populates="drug_quiz_option")

