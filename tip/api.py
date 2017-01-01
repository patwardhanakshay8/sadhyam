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
from tastypie import fields

from qresponse.models import *
from quiz.models import *
from quiz.api import *
from tip.models import *

from itertools import chain
from operator import itemgetter
import json

class TipResource(ModelResource):

	exam = fields.ForeignKey(ExamResource,attribute='exam')
	subject = fields.ForeignKey(SubjectResource,attribute='subject',null=True,full=True)
	chapter = fields.ForeignKey(ChapterResource,attribute='chapter',null=True,full=True)
	owner = fields.ForeignKey(UserResource,attribute='owner',null=True,full=True)

	class Meta:
		limit = 0
		queryset = Tip.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'tip'
		allowed_methods = ['get']
		filtering = {
			'exam' : ALL_WITH_RELATIONS,
			'subject' : ALL_WITH_RELATIONS,
			'chapter' : ALL_WITH_RELATIONS,
			'owner' : ALL_WITH_RELATIONS
		} 

	def prepend_urls(self):
		return [
			url(r'^(?P<resource_name>%s)/feed%s$' %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('feed'), name="api_feed"),
		]

	def feed(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		feed_list = []
		practice_result = PracticeResult.objects.all()
		for item in practice_result:
			practice_result_obj = {}
			practice_result_obj['feed_type'] = 'Result'
			practice_result_obj['subscriber'] = item.subscriber
			practice_result_obj['marks_obtained'] = item.marks_obtained
			practice_result_obj['total_marks'] = item.total_marks
			practice_result_obj['timestamp'] = item.timestamp
			feed_list.append(practice_result_obj)
		tip = Tip.objects.all()
		for item in tip:
			tip_obj = {}
			tip_obj['feed_type'] = 'Tip'
			tip_obj['exam'] = item.exam
			tip_obj['subject'] = item.subject
			tip_obj['chapter'] = item.chapter
			tip_obj['description'] = item.description
			tip_obj['owner'] = item.owner
			tip_obj['timestamp'] = item.timestamp
			feed_list.append(tip_obj)
		
		feed_list = sorted(feed_list,key=itemgetter("timestamp"))

		if request.user and request.user.is_authenticated():
			return self.create_response(request, {
				'success': True,
				'feed' : feed_list
			})			
		else:
			return self.create_response(request, {
				'success': False,
				}, HttpUnauthorized )
