from django.conf.urls import include, url
from tastypie.api import Api
from tip.api import *

v1_api = Api(api_name='v1')
v1_api.register(TipResource())

urlpatterns = [    
    url(r'^',include(v1_api.urls)),    
]


