from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from quiz.models import *
import time,random

# Create your models here.
class Subscriber(models.Model):
	user = models.ForeignKey(User)
	date_of_birth = models.DateField()
	profession = models.CharField(max_length=255,default='profession')
	educational_qualification = models.CharField(max_length=255,default='educational qualification')
	student = models.BooleanField(default=False)
	mentor = models.BooleanField(default=False)

	def __unicode__(self):
		return format(self.user)

class ExamSubscribed(models.Model):
	exam_subscribed = models.ForeignKey(Exam)
	subscriber = models.ForeignKey(Subscriber)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.subscriber)

class Test(models.Model):
	test_code = models.CharField(max_length=255,default='test_code',editable=False)
	test_template = models.ForeignKey(TestTemplate)
	subscriber = models.ForeignKey(Subscriber)
	number_of_question = models.FloatField(default=0.0)
	time_limit = models.FloatField(default=0.0)
	total_marks = models.FloatField(default=0.0)
	marks_obtained = models.FloatField(default=0.0)
	total_time_taken = models.FloatField(default=0.0)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return format(self.test_code)

	def save(self,*args,**kwargs):
		number_of_question = 0
		total_marks = 0
		time_limit = 0
		new_questions = []
		count = 0
		
		if self.test_code == 'test_code':
			self.test_code = str(int(time.time())) + (self.test_template.title)[:3].upper() + (self.subscriber.user.username)[:3].upper()

		test_template_details = TemplateDetail.objects.filter(test_template=self.test_template)
		from qresponse.models import QResponse
		prev_ques = QResponse.objects.filter(subscriber=self.subscriber,test_template=self.test_template).values('question')
		for t in test_template_details:
			if t.question:
				number_of_question += 1
				total_marks += t.correct_ans_marks
				if { 'question': t.question.id } not in prev_ques and t.question.id not in new_questions:
					new_questions.append({ 'question': t.question , 'correct_ans_marks': t.question.correct_ans_marks, 'wrong_ans_marks' : t.question.wrong_ans_marks })
			elif t.chapter:
				number_of_question += t.number_of_question
				total_marks += t.correct_ans_marks * t.number_of_question
				questions = Question.objects.filter(chapter=t.chapter,difficulty=t.difficulty,type_of_question=t.type_of_question)	
				for q in questions:
					if { 'question': q.id } not in prev_ques and q.id not in new_questions:
						if count < t.number_of_question:
							new_questions.append({ 'question': q , 'correct_ans_marks': t.correct_ans_marks, 'wrong_ans_marks' : t.wrong_ans_marks })
							count += 1
				count = 0

			elif t.subject:
				number_of_question += t.number_of_question
				total_marks += t.correct_ans_marks * t.number_of_question
				questions = Question.objects.filter(subject=t.subject,difficulty=t.difficulty,type_of_question=t.type_of_question)			
				for q in questions:
					if { 'question': q.id } not in prev_ques and q.id not in new_questions:
						if count < t.number_of_question:
							new_questions.append({ 'question': q , 'correct_ans_marks': t.correct_ans_marks, 'wrong_ans_marks' : t.wrong_ans_marks })
							count += 1
				count = 0
		if prev_ques:
			while len(new_questions) < number_of_question:
				random_ques = random.choice(prev_ques)['question']
				if random_ques not in new_questions:
					new_questions.append(Question.objects.get(id=random_ques))
		
		for q in new_questions:
			qresponse = QResponse()
			qresponse.test_code = self.test_code
			qresponse.subscriber = self.subscriber
			qresponse.test_template = self.test_template
			qresponse.question = q['question']
			qresponse.correct_ans_marks = q['correct_ans_marks']
			qresponse.wrong_ans_marks = q['wrong_ans_marks']
			qresponse.save()

		if self.test_template.time_limit_type == 'Hrs':
			time_limit += (t.test_template.time_limit * 60)
		else:
			time_limit += t.test_template.time_limit
		self.number_of_question = number_of_question
		self.total_marks = total_marks
		self.time_limit = time_limit
		super(Test,self).save(*args,**kwargs)
