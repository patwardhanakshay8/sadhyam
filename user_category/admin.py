from django.contrib import admin
from user_category.models import *

# Register your models here.
class SubscriberAdmin(admin.ModelAdmin):
	list_display = ('user','profession','student','mentor',)
	search_fields = ('user__username',)

class ExamSubscribedAdmin(admin.ModelAdmin):
	list_display = ('exam_subscribed','subscriber',)
	list_filter = ('subscriber',)

class TestAdmin(admin.ModelAdmin):
	list_display = ('test_code','test_template','subscriber','number_of_question','time_limit','total_marks','marks_obtained','total_time_taken',)
	list_filter = ('test_template','subscriber',)

admin.site.register(Subscriber,SubscriberAdmin)
admin.site.register(ExamSubscribed,ExamSubscribedAdmin)
admin.site.register(Test,TestAdmin)
