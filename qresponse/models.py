from __future__ import unicode_literals

from django.db import models
from quiz.models import *
from user_category.models import *

# Create your models here.
class QResponse(models.Model):
	test_code = models.CharField(max_length=255,default='test_code')
	subscriber = models.ForeignKey(Subscriber)
	test_template = models.ForeignKey(TestTemplate)
	question = models.ForeignKey(Question)
	response = models.CharField(max_length=255,default='response')
	correct = models.BooleanField(default=False)
	correct_ans_marks = models.FloatField(default=0.0)
	wrong_ans_marks = models.FloatField(default=0.0)
	marks_obtained = models.FloatField(default=0.0)
	time_taken = models.FloatField(default=0.0)
	timestamp = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return format(self.test_code)

