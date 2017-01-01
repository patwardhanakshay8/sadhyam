"""sadhyam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from quiz import urls
from user_category import urls
from qresponse import urls
from tip import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/quiz/',include('quiz.urls')),
    url(r'^api/subscriber/',include('user_category.urls')),
    url(r'^api/qresponse/',include('qresponse.urls')),
    url(r'^api/tip/',include('tip.urls')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^redactor/', include('redactor.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
