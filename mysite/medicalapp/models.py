import os
from django.db import models
from django.contrib.auth.models import User

class DrugClass(models.Model):
  class Meta:
    db_table = "drug_class"
  drug_class_id = models.AutoField(primary_key=True)
  drug_class_name = models.CharField(max_length=50)
  drug_class_description = models.CharField(max_length=200)

  def __str__(self):
    return self.drug_class_name

class DrugSubClass(models.Model):
  class Meta:
    db_table = "drug_subclass"  
  drug_subclass_id = models.AutoField(primary_key=True)
  drug_class = models.ForeignKey(DrugClass, null=True, on_delete=models.SET_NULL)
  drug_subclass_name = models.CharField(max_length=50)
  drug_subclass_description = models.CharField(max_length=200)

  def __str__(self):
      return self.drug_subclass_name

class Drug(models.Model):
  class Meta:
    db_table = "drug"
  drug_id = models.AutoField(primary_key=True)
  drug_subclass = models.ForeignKey(DrugSubClass, null=True, on_delete=models.SET_NULL)
  drug_name = models.CharField(max_length=256)
  black_box_warning = models.CharField(max_length=500)

  def __str__(self):
    return self.drug_name

class DrugInformationType(models.Model):
  class Meta:
    db_table = "drug_information_type"
  drug_info_type_id = models.AutoField(primary_key=True)
  drug_information_type = models.CharField(max_length=50)
  game_level = models.IntegerField(default=0)

  def __str__(self):
    return self.drug_information_type

class DrugKeyword(models.Model):
  class Meta:
    db_table = "drug_keyword"
  keyword_id = models.AutoField(primary_key=True)
  keyword = models.CharField(max_length=256)

  def __str__(self):
    return self.keyword

class DrugInformation(models.Model):
  class Meta:
    db_table = "drug_information"
  drug_info_id = models.AutoField(primary_key=True)
  drug = models.ForeignKey(Drug, null=True, on_delete=models.SET_NULL)
  drug_info_type = models.ForeignKey(DrugInformationType, null=True, on_delete=models.SET_NULL)
  information = models.CharField(max_length=1024)
  scrabble_hint = models.CharField(max_length=1024)
  keyword_bk = models.CharField(max_length=1024)
  keyword = models.ManyToManyField(DrugKeyword, through='DrugInformationKeyword')

  def __str__(self):
    return str(self.drug.drug_id) + " : " + str(self.drug_info_type.drug_info_type_id) + " : " + self.information

class DrugInformationKeyword(models.Model):
  class Meta:
    db_table = "drug_info_keyword"
  relation_id = models.AutoField(primary_key=True)
  drug_info = models.ForeignKey(DrugInformation, on_delete= models.CASCADE)
  keyword = models.ForeignKey(DrugKeyword, on_delete= models.CASCADE)

  def __str__(self):
    return str(self.drug_info.drug_info_id) + " : " + str(self.keyword.keyword)

class DrugQuizQuestion(models.Model):
  class Meta:
    db_table = "drug_quiz_question"
  drug_quiz_id = models.AutoField(primary_key=True)
  drug = models.ForeignKey(Drug, null=True, on_delete=models.SET_NULL)
  drug_info_type = models.ForeignKey(DrugInformationType, null=True, on_delete=models.SET_NULL)
  quiz_question = models.CharField(max_length=500)
  quiz_type = models.CharField(max_length=500)
  enable = models.BooleanField()

  def __str__(self):
    return str(self.drug_quiz_id) + " : " + self.quiz_question

class DrugQuizOption(models.Model):
  class Meta:
    db_table = "drug_quiz_option"
  quiz_option_id = models.AutoField(primary_key=True)
  quiz = models.ForeignKey(DrugQuizQuestion, null=True, on_delete=models.SET_NULL)
  quiz_option = models.CharField(max_length=200)
  correct_flag = models.BooleanField()

  def __str__(self):
    return str(self.quiz.drug_quiz_id) + " : " + self.quiz_option
