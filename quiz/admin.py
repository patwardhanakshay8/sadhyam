from django import forms
from redactor.widgets import RedactorEditor
from django.contrib import admin
from quiz.models import *

# Register your models here.

class ExamAdmin(admin.ModelAdmin):
	list_display = ('title',)
	search_fields = ('title',)

class SubjectAdmin(admin.ModelAdmin):
	list_display = ('exam','title',)
	list_filter = ('exam',)
	search_fields = ('exam__title','title',)

class ChapterAdmin(admin.ModelAdmin):
	list_display = ('exam','subject','title',)
	list_filter = ('exam','subject',)
	search_fields = ('exam__title','subject__title','title',)

class QuestionAdminForm(forms.ModelForm):
	
	class Meta:
		model = Question
		fields = ('exam','subject','chapter','difficulty','question','correct_ans','correct_ans_marks','wrong_ans_marks','type_of_question','solution',)
		widgets = {
		   'question': RedactorEditor(),
		   'solution': RedactorEditor(),
		}

class QuestionAdmin(admin.ModelAdmin):
	form = QuestionAdminForm
	list_display = ('exam','subject','chapter','difficulty','question','correct_ans','correct_ans_marks','wrong_ans_marks','type_of_question','owner',)
	list_filter = ('exam','subject','chapter','owner',)

	def save_model(self, request, obj, form, change):
		if not change:
			obj.owner = request.user
		obj.save()


class TemplateDetailInline(admin.StackedInline):
	model =  TemplateDetail
	extra = 1

class TestTemplateAdmin(admin.ModelAdmin):
	inlines = [TemplateDetailInline]
	excludes = ('owner',)
	list_display = ('title','time_limit','time_limit_type','owner',)
	list_filter = ('owner',)

	def save_model(self, request, obj, form, change):
		if not change:
			obj.owner = request.user
		obj.save()



admin.site.register(Exam,ExamAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(TestTemplate,TestTemplateAdmin)

