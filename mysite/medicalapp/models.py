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

