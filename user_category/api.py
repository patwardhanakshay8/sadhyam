from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.db import IntegrityError
from django.db.models import Sum

from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpResponse
from tastypie.resources import ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization,Authorization
from tastypie.utils import trailing_slash
from tastypie import fields

from user_category.models import *
from quiz.models import *
from quiz.api import *
from qresponse.models import *
import json

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		fields = ['first_name', 'last_name', 'email']
		allowed_methods = ['get', 'post']
		# authorization = DjangoAuthorization()
		resource_name = 'user'

	def prepend_urls(self):
		return [
			url(r'^(?P<resource_name>%s)/login%s$' %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('login'), name="api_login"),
			url(r'^(?P<resource_name>%s)/logout%s$' %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('logout'), name='api_logout'),
			url(r'^(?P<resource_name>%s)/update_profile%s$' %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('update_profile'), name='api_update_profile'),
		]

	def obj_create(self, bundle, request=None, **kwargs):
		username, password, first_name, last_name, email = bundle.data['username'], bundle.data['password'], bundle.data['first_name'], bundle.data['last_name'], bundle.data['email']
		try:
			bundle.obj = User.objects.create_user(username, email , password, first_name, last_name)
			if bundle.obj:
				subscriber = Subscriber()
				subscriber.user = bundle.obj
				subscriber.date_of_birth = bundle.data['date_of_birth']
				subscriber.profession = bundle.data['profession']
				subscriber.educational_qualification = bundle.data['educational_qualification']
				if bundle.data['student']:
					subscriber.student = bundle.data['student']
				elif bundle.data['mentor']:
					subscriber.mentor = bundle.data['mentor']
				else:
					subscriber.student = True
				subscriber.save()
		except IntegrityError:
			raise BadRequest('That username already exists')
		return bundle

	def login(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		data = json.loads(request.body)
		username = data["username"]
		password = data["password"]
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return self.create_response(request, {
					'success': True
				})
			else:
				return self.create_response(request, {
					'success': False,
					'reason': 'disabled',
					}, HttpForbidden )
		else:
			return self.create_response(request, {
				'success': False,
				'reason': 'incorrect',
				}, HttpUnauthorized )

	def logout(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		if request.user and request.user.is_authenticated():
			logout(request)
			return self.create_response(request, { 'success': True })
		else:
			return self.create_response(request, { 'success': False }, HttpUnauthorized)

	def update_profile(self,request,**kwargs):
		self.method_check(request,allowed=['post'])
		data = json.loads(request.body)
		updated_data = {}
		if request.user and request.user.is_authenticated():
			subscriber = Subscriber.objects.get(user=request.user)
			if 'date_of_birth' in data:
				subscriber.date_of_birth = data['date_of_birth']
				updated_data['date_of_birth'] = True
			elif 'profession' in data:
				subscriber.profession = data['profession']
				updated_data['profession'] = True
			elif 'educational_qualification' in data:
				subscriber.educational_qualification = data['educational_qualification']
				updated_data['educational_qualification'] = True
			elif 'student' in data:
				subscriber.student = data['student']
				updated_data['student'] = True
			elif 'mentor' in data:
				subscriber.mentor = data['mentor']
				updated_data['mentor'] = True
			subscriber.save()
			return self.create_response(request, { 'success': True,'updated_data':updated_data })
		else:
			return self.create_response(request, { 'success': False },HttpUnauthorized)


class SubscriberResource(ModelResource):
	user = fields.ForeignKey(UserResource,attribute='user')

	class Meta:
		limit = 0
		queryset = Subscriber.objects.all()
		authentication = Authentication()
		authorization = Authorization()
		resource_name = 'subscriber'
		allowed_methods = ['get']
		excludes = ['timestamp']
		filtering = {
			'student' : ALL,
			'mentor' : ALL
		}

	def dehydrate(self,bundle):
		bundle.data['user'] = bundle.obj.user.username
		return bundle

class ExamSubscribedResource(ModelResource):
	subscriber = fields.ForeignKey(SubscriberResource,attribute='subscriber')
	exam_subscribed = fields.ForeignKey(ExamResource,attribute='exam_subscribed')
	class Meta:
		limit = 0
		queryset = ExamSubscribed.objects.all()
		authentication = Authentication()
		authorization = Authorization()
		resource_name = 'exam_subscribed'
		allowed_methods = ['get','post','delete']
		excludes = ['timestamp']
		filtering = {
			'exam' : ALL_WITH_RELATIONS,
			'subscriber' : ALL_WITH_RELATIONS
		}

	def dehydrate(self,bundle):
		bundle.data['subscriber'] = bundle.obj.subscriber.user.username
		bundle.data['exam_subscribed'] = bundle.obj.exam_subscribed.title
		return bundle

	def obj_create(self, bundle,request=None,**kwargs):
		subscriber = bundle.data['subscriber']
		exam_subscribed = bundle.data['exam_subscribed']

		if subscriber and exam_subscribed:
			if bundle.request.user and bundle.request.user.is_authenticated():
				subscriber = Subscriber.objects.get(user__username=subscriber)
				exam = Exam.objects.get(title=exam_subscribed)
				exam_subscribed = ExamSubscribed.objects.filter(subscriber=subscriber,exam_subscribed=exam)
				if not exam_subscribed:
					bundle.obj = ExamSubscribed.objects.create(subscriber=subscriber,exam_subscribed=exam)
				else:
					raise BadRequest('You have already subscribed to this exam.')
			else:
				raise BadRequest('Unauthorized!')
		else:
			raise BadRequest('Fields are missing!')
		return bundle

class TestResource(ModelResource):
	test_template = fields.ForeignKey(TestTemplateResource,attribute='test_template')
	subscriber = fields.ForeignKey(SubscriberResource,attribute='subscriber')

	class Meta:
		limit = 0 
		queryset = Test.objects.all()
		authentication = Authentication()
		authorization = Authorization()
		resource_name = 'test'
		allowed_methods = ['get','post','delete']
		excludes = ['timestamp']
		filtering = {
			'test_template' : ALL_WITH_RELATIONS,
			'subscriber' : ALL_WITH_RELATIONS
		}

	def prepend_urls(self):
		return [
			url(r'^(?P<resource_name>%s)/submit_test%s$' %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('submit_test'), name="api_submit_test"),
		]

	def dehydrate(self,bundle):
		bundle.data['test_template'] = bundle.obj.test_template.title
		bundle.data['subscriber'] = bundle.obj.subscriber.user.username
		return bundle

	def obj_create(self,bundle,request=None,**kwargs):
		test_template = bundle.data['test_template']
		subscriber = bundle.data['subscriber']

		if test_template and subscriber:
			if bundle.request.user and bundle.request.user.is_authenticated():
				test_template = TestTemplate.objects.get(title=test_template)
				subscriber = Subscriber.objects.get(user__username=subscriber)
				bundle.obj = Test.objects.create(test_template=test_template,subscriber=subscriber)
			else:
				raise BadRequest('Unauthorized!')
		else:
			raise BadRequest('Fields are missing!')
		return bundle			

	def submit_test(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		data = json.loads(request.body)
		if data['test_code'] and data['subscriber']:
			if request.user and request.user.is_authenticated():
				subscriber = Subscriber.objects.get(user__username=data['subscriber'])
				test_submit = Test.objects.filter(test_code=data['test_code'],subscriber=subscriber)
				if test_submit:				
					marks_obtained = QResponse.objects.filter(test_code=data['test_code'],subscriber=subscriber).aggregate(Sum('marks_obtained'))
					if marks_obtained["marks_obtained__sum"]:
						marks_obtained = marks_obtained["marks_obtained__sum"]
						print type(marks_obtained)
					total_time_taken = QResponse.objects.filter(test_code=data['test_code'],subscriber=subscriber).aggregate(Sum('time_taken'))
					if total_time_taken["time_taken__sum"]:
						total_time_taken_in_mins = (total_time_taken["time_taken__sum"]) / 60
						total_time_taken = total_time_taken_in_mins
					test_submit.update(marks_obtained=float(marks_obtained),total_time_taken=float(total_time_taken))
				return self.create_response(request, {'success': True,'subscriber': test_submit[0].subscriber,'test_code': test_submit[0].test_code,'total_marks':test_submit[0].total_marks,'marks_obtained': test_submit[0].marks_obtained, 'time_limit':test_submit[0].time_limit, 'total_time_taken': test_submit[0].total_time_taken })
		else:
			return self.create_response(request, {'success': False}, HttpUnauthorized)





