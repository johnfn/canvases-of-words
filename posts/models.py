from django.db import models
from django.contrib.auth.models import User
from canvases.groups.models import Group

class Post(models.Model):
  title   = models.CharField(max_length=1000)
  creator = models.ForeignKey(User)
  group   = models.ForeignKey(Group)
  content = models.TextField()
  date    = models.DateTimeField('date published')
  visible = models.BooleanField()
  
  def __unicode__(self):
    return self.content

class Response(models.Model):
  creator = models.ForeignKey(User)
  parent  = models.ForeignKey(Post)
  content = models.TextField()

  def __unicode__(self):
    return self.content