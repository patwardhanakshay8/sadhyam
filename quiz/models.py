from __future__ import unicode_literals

from django.db import models
from smart_selects.db_fields import ChainedForeignKey 
from django.contrib.auth.models import User

# Choices
DIFFICULTY = (
	('Low','Low'),
	('Moderate','Moderate'),
	('High','High'),
	)

TYPE_OF_QUESTION = (
	('Practice','Practice'),
	('Test','Test'),
	)

TIME_LIMIT_TYPE = (
	('Mins','Mins'),
	('Hrs','Hrs'),
	)


# Create your models here.
class Exam(models.Model):
	title = models.CharField(max_length=255,default='Exam')
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.title)

class Subject(models.Model):
	exam = models.ForeignKey(Exam)
	title = models.CharField(max_length=255,default='Subject')
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.title)

class Chapter(models.Model):
	exam = models.ForeignKey(Exam)
	subject = ChainedForeignKey(Subject, chained_field="exam", chained_model_field="exam")
	title = models.CharField(max_length=255,default='Chapter')
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.title)

class Question(models.Model):
	exam = models.ForeignKey(Exam)
	subject = ChainedForeignKey(Subject,chained_field="exam",chained_model_field="exam",blank=True,null=True)
	chapter = ChainedForeignKey(Chapter,chained_field="subject",chained_model_field="subject",blank=True,null=True)
	difficulty = models.CharField(max_length=255,default='Low',choices=DIFFICULTY)
	question = models.TextField()
	correct_ans = models.CharField(max_length=255,default='correct answer')
	correct_ans_marks = models.FloatField(default=0.0)
	wrong_ans_marks = models.FloatField(default=0.0)
	type_of_question = models.CharField(max_length=255,default='Practice',choices=TYPE_OF_QUESTION)
	solution = models.TextField()
	owner = models.ForeignKey(User,editable=False)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.question)

class TestTemplate(models.Model):
	title = models.CharField(max_length=255,default='Test Template')
	time_limit = models.FloatField(default=0.0)
	time_limit_type = models.CharField(max_length=255,default='Mins',choices=TIME_LIMIT_TYPE)
	owner = models.ForeignKey(User,editable=False)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.title)

class TemplateDetail(models.Model):
	test_template = models.ForeignKey(TestTemplate)
	exam = models.ForeignKey(Exam)
	subject = ChainedForeignKey(Subject,chained_field="exam",chained_model_field="exam",blank=True,null=True)
	chapter = ChainedForeignKey(Chapter,chained_field="subject",chained_model_field="subject",blank=True,null=True)
	question = models.ForeignKey(Question,blank=True,null=True)
	difficulty = models.CharField(max_length=255,default='Low',choices=DIFFICULTY)
	type_of_question = models.CharField(max_length=255,default='Test',choices=TYPE_OF_QUESTION)
	number_of_question = models.FloatField(default=0.0)
	correct_ans_marks = models.FloatField(default=0.0)
	wrong_ans_marks = models.FloatField(default=0.0)
	owner = models.ForeignKey(User,editable=False)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.test_template)

	def save(self,*args,**kwargs):
		if self.question:
			self.difficulty = self.question.difficulty
			self.type_of_question = self.question.type_of_question
			self.correct_ans_marks = self.question.correct_ans_marks
			self.wrong_ans_marks = self.question.wrong_ans_marks
		self.owner = self.test_template.owner
		super(TemplateDetail,self).save(*args,**kwargs)
