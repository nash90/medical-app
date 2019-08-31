import os
from django.db import models

from django.contrib import auth
from .models import MyUser

class Profile(models.Model):
  class Meta:
    db_table = 'profile'
  profile_id = models.AutoField(primary_key=True)
  user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
  date_of_birth = models.DateField()