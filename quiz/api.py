from django.contrib.auth.models import User
from django.conf.urls import url

from tastypie import fields
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.authentication import Authentication,ApiKeyAuthentication,MultiAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization
from tastypie.models import *
from tastypie.utils import trailing_slash

from quiz.models import *

class UserResource(ModelResource):

	class Meta:
		limit = 0
		queryset = User.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'user'
		allowed_methods = ['get']
		fields = ['id','username','email','first_name','last_name']
		filtering = {
			'username' : ALL,
		}


class ExamResource(ModelResource):

	class Meta:
		limit = 0
		queryset = Exam.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'exam'
		allowed_methods = ['get','post']
		excludes = ['timestamp']
		filtering = {
			'title' : ALL,
		}

class SubjectResource(ModelResource):

	exam = fields.ForeignKey(ExamResource,attribute='exam')

	class Meta:
		limit = 0
		queryset = Subject.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'subject'
		allowed_methods = ['get','post']
		excludes = ['timestamp']
		filtering = {
			'exam' : ALL_WITH_RELATIONS,
			'title' : ALL,
		}

	def dehydrate(self,bundle):
		bundle.data['exam'] = bundle.obj.exam.title
		return bundle

	def obj_create(self, bundle,request=None,**kwargs):
		exam = bundle.data['exam']
		subject = bundle.data['subject']

		if exam and subject:
			if ApiKey.objects.filter(user__username=request.GET['username'],key=request.GET['api_key']):
				exam = Exam.objects.get(title=exam)
				if exam:
					subject = Subject.objects.create(exam=exam,title=subject)
				else:
					raise BadRequest('Exam does not exist.')
			else:
				raise BadRequest('User is not authenticated.')
		else:
			raise BadRequest('Field is missing.')

class ChapterResource(ModelResource):

	subject = fields.ForeignKey(SubjectResource,attribute='subject')

	class Meta:
		limit = 0
		queryset = Chapter.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'chapter'
		allowed_methods = ['get','post']
		excludes = ['timestamp']
		filtering = {
			'subject' : ALL_WITH_RELATIONS,
			'title' : ALL,
		}

	def dehydrate(self,bundle):
		bundle.data['subject'] = bundle.obj.subject.title
		return bundle

	def obj_create(self,bundle,request=None,**kwargs):
		subject = bundle.data['subject']
		chapter = bundle.data['chapter']

		if subject and chapter:
			if ApiKey.objects.filter(user__username=request.GET['username'],key=request.GET['api_key']):
				subject = Subject.objects.get(title=subject)
				if subject:
					chapter = Chapter.objects.create(exam=subject.exam,subject=subject,title=chapter)
				else:
					raise BadRequest('Subject does not exist')
			else:
				raise BadRequest('User is not authenticated.')
		else:
			raise BadRequest('Field is missing.')

class QuestionResource(ModelResource):

	exam = fields.ForeignKey(ExamResource,attribute='exam')
	subject = fields.ForeignKey(SubjectResource,attribute='subject',null=True,blank=True)
	chapter = fields.ForeignKey(ChapterResource,attribute='chapter',null=True,blank=True)
	owner = fields.ForeignKey(UserResource,attribute='owner')

	class Meta:
		limit = 0
		queryset = Question.objects.order_by('-timestamp')
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'question'
		allowed_methods = ['get','post','put','delete']
		# excludes = ['timestamp']
		filtering = {
			'exam' : ALL_WITH_RELATIONS,
			'subject' : ALL_WITH_RELATIONS,
			'chapter' : ALL_WITH_RELATIONS,
			'owner' : ALL_WITH_RELATIONS,
			'type_of_question' : ALL,
		}

	def get_object_list(self, request):
		if 'number_of_question' in request.GET:
			number_of_question = request.GET['number_of_question']
			return super(QuestionResource,self).get_object_list(request)[:number_of_question]
		else:
			return super(QuestionResource,self).get_object_list(request)

	def dehydrate(self,bundle):
		bundle.data['exam'] = bundle.obj.exam.title
		if bundle.obj.subject:
			bundle.data['subject'] = bundle.obj.subject.title
		else:
			bundle.data['subject'] = ''
		if bundle.obj.chapter:
			bundle.data['chapter'] = bundle.obj.chapter.title
		else:
			bundle.data['chapter'] = ''
		bundle.data['owner'] = bundle.obj.owner.username
		return bundle

	def obj_create(self,bundle,request=None,**kwargs):
		difficulty = bundle.data['difficulty']
		exam = bundle.data['exam']
		chapter = bundle.data['chapter']
		subject = bundle.data['subject']
		question = bundle.data['question']
		correct_ans = bundle.data['correct_ans']
		correct_ans_marks = bundle.data['correct_ans']
		wrong_ans_marks = bundle.data['wrong_ans_marks']
		type_of_question = bundle.data['type_of_question']
		solution = bundle.data['solution']

		if difficulty and question and correct_ans and correct_ans_marks and wrong_ans_marks and type_of_question and solution:
			if ApiKey.objects.filter(user__username=request.GET['username'],key=request.GET['api_key']):
				if chapter:
					chapter = Chapter.objects.get(title=chapter)
					if chapter:
						question = Question()
						question.exam = chapter.subject.exam
						question.subject = chapter.subject
						question.chapter = chapter
						question.difficulty = difficulty
						question.question = question
						question.correct_ans = correct_ans
						question.correct_ans_marks = correct_ans_marks
						question.wrong_ans_marks = wrong_ans_marks
						question.type_of_question = type_of_question
						question.solution = solution
						question.owner = bundle.request.user
					else:
						raise BadRequest('Chapter does not exist.')
				elif subject:
					subject = Subject.objects.get(title=subject)
					if subject:
						question = Question()
						question.exam = subject.exam
						question.subject = subject
						# question.chapter = chapter
						question.difficulty = difficulty
						question.question = question
						question.correct_ans = correct_ans
						question.correct_ans_marks = correct_ans_marks
						question.wrong_ans_marks = wrong_ans_marks
						question.type_of_question = type_of_question
						question.solution = solution
						question.owner = bundle.request.user
					else:
						raise BadRequest('Subject does not exist.')
				elif exam:
					exam = Exam.objects.get(title=exam)
					if exam:
						question = Question()
						question.exam = exam
						# question.subject = chapter.subject
						# question.chapter = chapter
						question.difficulty = difficulty
						question.question = question
						question.correct_ans = correct_ans
						question.correct_ans_marks = correct_ans_marks
						question.wrong_ans_marks = wrong_ans_marks
						question.type_of_question = type_of_question
						question.solution = solution
						question.owner = bundle.request.user
					else:
						raise BadRequest('Exam does not exist.')				
			else:
				raise BadRequest('User is not authenticated.')
		else:
			raise BadRequest('Some fields are missing.')

		return bundle


class TestTemplateResource(ModelResource):

	owner = fields.ForeignKey(UserResource,attribute='owner')

	class Meta:
		limit = 0
		queryset = TestTemplate.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'test_template'
		fields = ['title','time_limit','time_limit_type','owner__username']
		allowed_methods = ['get','post','put','delete']
		filtering = {
			'owner' : ALL_WITH_RELATIONS,
			'title' : ALL,
		}

	def dehydrate(self,bundle):
		bundle.data['owner'] = bundle.obj.owner.username
		return bundle

	def obj_create(self,bundle,request=None,**kwargs):
		title = bundle.data['title']
		time_limit = bundle.data['time_limit']
		time_limit_type = bundle.data['time_limit_type']

		if title and time_limit and time_limit_type:
			if ApiKey.objects.filter(user__username=request.GET['username'],key=request.GET['api_key']):
				test_template = TestTemplate()
				test_template.title = title
				test_template.time_limit = time_limit
				test_template.time_limit_type = time_limit_type
				test_template.owner = bundle.request.user
				test_template.save()
			else:
				raise BadRequest('User is not authenticated.')
		else:
			raise BadRequest('Some field is missing.')
		return bundle

class TemplateDetailResource(ModelResource):

	test_template = fields.ForeignKey(TestTemplateResource,attribute='test_template',full=True)
	exam = fields.ForeignKey(ExamResource,attribute='exam',full=True,null=True)
	subject = fields.ForeignKey(SubjectResource,attribute='subject',full=True,null=True)
	chapter = fields.ForeignKey(ChapterResource,attribute='chapter',full=True,null=True)
	question = fields.ForeignKey(QuestionResource,attribute='question',full=True,null=True)
	owner = fields.ForeignKey(UserResource,attribute='owner',full=True)

	class Meta:
		limit = 0
		queryset = TemplateDetail.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		resource_name = 'template_detail'
		allowed_methods = ['get','post','put','delete']
		excludes = ['timestamp']
		filtering = {
			'test_template' : ALL_WITH_RELATIONS,
			'exam' : ALL_WITH_RELATIONS,
			'subject' : ALL_WITH_RELATIONS,
			'chapter' : ALL_WITH_RELATIONS,
			'owner' : ALL_WITH_RELATIONS,
		}

	def dehydrate(self,bundle):
		bundle.data['test_template'] = bundle.obj.test_template.title
		if bundle.obj.exam:
			bundle.data['exam'] = bundle.obj.exam.title
		else:
			bundle.data['exam'] = ''
		if bundle.obj.subject:
			bundle.data['subject'] = bundle.obj.subject.title
		else:
			bundle.data['subject'] = ''
		if bundle.obj.chapter:
			bundle.data['chapter'] = bundle.obj.chapter.title
		else:
			bundle.data['chapter'] = ''
		if bundle.obj.question:
			bundle.data['question'] = bundle.obj.question.question
		else:
			bundle.data['question'] = ''
		bundle.data['owner'] = bundle.obj.owner.username
		return bundle

	def obj_create(self,bundle,request=None,**kwargs):
		test_template = bundle.data['test_template']
		exam = bundle.data['exam']
		subject = bundle.data['subject']
		chapter = bundle.data['chapter']
		question_id = bundle.data['question_id']
		difficulty = bundle.data['difficulty']
		type_of_question = bundle.data['type_of_question']
		number_of_question = bundle.data['number_of_question']
		correct_ans_marks = bundle.data['correct_ans_marks']
		wrong_ans_marks = bundle.data['wrong_ans_marks']

		if test_template:
			if ApiKey.objects.filter(user__username=request.GET['username'],key=request.GET['api_key']):
				if exam or subject or chapter:
					if difficulty and type_of_question and number_of_question:
						template_detail = TemplateDetail()
						template_detail.test_template = test_template
						if exam:
							template_detail.exam = Exam.objects.get(title=exam)
						elif subject:
							template_detail.subject = Subject.objects.get(title=subject)
						elif chapter:
							template_detail.chapter = Chapter.objects.get(title=chapter)
						template_detail.difficulty = difficulty
						template_detail.type_of_question = type_of_question
						template_detail.number_of_question = number_of_question
						if correct_ans_marks and wrong_ans_marks:
							template_detail.correct_ans_marks = correct_ans_marks
							template_detail.wrong_ans_marks = wrong_ans_marks
						template_detail.owner = bundle.request.user
					else:
						raise BadRequest('Some fields are missing.')
				elif question:
					template_detail = TemplateDetail()
					template_detail.question = question
					template_detail.owner = bundle.request.user
			else:
				raise BadRequest('User is not authenticated.')
		else:
			raise BadRequest('Test template is not chosen.')

		return bundle



