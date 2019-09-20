import os
from django.db import models
from django.contrib import auth

from .models import GameBadge
User = auth.get_user_model()

class Profile(models.Model):
  class Meta:
    db_table = 'profile'
  profile_id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  date_of_birth = models.DateField()

class UserPoints(models.Model):
  class Meta:
    db_table = 'user_points'
  user_points_id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  points = models.IntegerField()
  badge = models.ForeignKey(GameBadge, null=True, on_delete=models.SET_NULL)

  def __str__(self):
    return self.user.email