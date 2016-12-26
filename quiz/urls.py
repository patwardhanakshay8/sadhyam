from django.conf.urls import include, url
from tastypie.api import Api
from quiz.api import *

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ExamResource())
v1_api.register(SubjectResource())
v1_api.register(ChapterResource())
v1_api.register(QuestionResource())
v1_api.register(TestTemplateResource())
v1_api.register(TemplateDetailResource())

urlpatterns = [    
    url(r'^',include(v1_api.urls)),    
]


