from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
  name  =       models.CharField(max_length=100)
  description = models.TextField()
  users =       models.ManyToManyField(User)