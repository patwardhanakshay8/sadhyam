from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from quiz.models import *

# Create your models here.
class Tip(models.Model):
	exam = models.ForeignKey(Exam)
	subject = models.ForeignKey(Subject,blank=True,null=True)
	chapter = models.ForeignKey(Chapter,blank=True,null=True)
	description = models.TextField()
	owner = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.exam)
