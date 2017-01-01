from django import forms
from redactor.widgets import RedactorEditor
from django.contrib import admin
from tip.models import *
# Register your models here.
class TipAdminForm(forms.ModelForm):
	
	class Meta:
		model = Tip
		fields = ('exam','subject','chapter','description','owner',)
		widgets = {
		   'description': RedactorEditor(),
		}

class TipAdmin(admin.ModelAdmin):
	form = TipAdminForm
	list_display = ('exam','subject','chapter','description','owner','timestamp',)

admin.site.register(Tip,TipAdmin)