from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
  creator = models.ForeignKey(User)
  content = models.TextField()
  date = models.DateTimeField('date published')

  def __unicode__(self):
    return self.content

class Response(models.Model):
  creator = models.ForeignKey(User)
  parent = models.ForeignKey(Post)
  content = models.TextField()

  def __unicode__(self):
    return self.content
