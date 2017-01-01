from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.db import IntegrityError

from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpResponse
from tastypie.resources import ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.authentication import Authentication,ApiKeyAuthentication,MultiAuthentication
from tastypie.authorization import DjangoAuthorization,Authorization
from tastypie.utils import trailing_slash
from tastypie.models import *
from tastypie import fields

from qresponse.models import *
from user_category.models import *
from user_category.api import *
from quiz.models import *
from quiz.api import *
import json

class QResponseResource(ModelResource):
	subscriber = fields.ForeignKey(SubscriberResource,attribute='subscriber')			
	test_template = fields.ForeignKey(TestTemplateResource,attribute='test_template')
	question = fields.ForeignKey(QuestionResource,attribute='question')

	class Meta:
		limit = 0
		queryset = QResponse.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'qresponse'
		allowed_methods = ['get','post']
		filtering = {
			'test_code': ALL,
			'subscriber': ALL_WITH_RELATIONS,
			'test_template': ALL_WITH_RELATIONS,
			'question' : ALL_WITH_RELATIONS
		}

	def dehydrate(self,bundle):
		bundle.data['subscriber'] = bundle.obj.subscriber.user.username
		bundle.data['test_template'] = bundle.obj.test_template.title
		bundle.data['question_id'] = bundle.obj.question.id
		bundle.data['question'] = bundle.obj.question.question
		return bundle

	def obj_create(self, bundle,request=None,**kwargs):
		response_obj = bundle.data['response_obj']
		
		if response_obj:
			if ApiKey.objects.filter(user__username=bundle.request.GET['username'],key=bundle.request.GET['api_key']):
				for r in response_obj:
					qresponse = QResponse.objects.get(test_code=r['test_code'],question__id=r['question_id'])
					qresponse.response = r['response']
					qresponse.time_taken = r['time_taken']
					question = Question.objects.get(id=r['question_id'])
					if r['response'] == question.correct_ans:
						qresponse.correct = True
						qresponse.marks_obtained += qresponse.correct_ans_marks
					else:
						qresponse.marks_obtained -= qresponse.wrong_ans_marks
					qresponse.save()
			else:
				raise BadRequest('That user is not authenticated.')
		else:
			raise BadRequest('Fields are missing.')

		return bundle

class PracticeResultResource(ModelResource):
	subscriber = fields.ForeignKey(SubscriberResource,attribute='subscriber')

	class Meta:
		limit = 0
		queryset = PracticeResult.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'practice_result'
		allowed_methods = ['get','post']
		filtering = {
			'subscriber' : ALL_WITH_RELATIONS,
			'timestamp' : ALL,

		}

	def dehydrate(self,bundle):
		bundle.data['subscriber'] = bundle.obj.subscriber.user.username
		return bundle

	def obj_create(self,bundle,request=None,**kwargs):
		subscriber = bundle.data['subscriber']
		marks_obtained = bundle.data['marks_obtained']
		total_marks = bundle.data['total_marks']

		if subscriber and marks_obtained and total_marks:
			if ApiKey.objects.filter(user__username=bundle.request.GET['username'],key=bundle.request.GET['api_key']):
				subscriber = Subscriber.objects.get(user__username=subscriber)
				if subscriber:
					practice_result = PracticeResult()
					practice_result.subscriber = subscriber
					practice_result.marks_obtained = marks_obtained
					practice_result.total_marks = total_marks
					practice_result.save()
				else:
					raise BadRequest('Subscriber does not exist.')
			else:
				raise BadRequest('User is not authenticated.')
		else:
			raise BadRequest('Fields are missing.')

		return bundle











