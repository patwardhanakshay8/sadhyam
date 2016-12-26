from django.conf.urls import include, url
from tastypie.api import Api
from user_category.api import *

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(SubscriberResource())
v1_api.register(ExamSubscribedResource())
v1_api.register(TestResource())

urlpatterns = [    
    url(r'^',include(v1_api.urls)),    
]


