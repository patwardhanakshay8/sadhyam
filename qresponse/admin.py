from django.contrib import admin
from qresponse.models import *
# Register your models here.
class QResponseAdmin(admin.ModelAdmin):
	list_display = ('test_code','subscriber','test_template','question','timestamp',)

class PracticeResultAdmin(admin.ModelAdmin):
	list_display = ('subscriber','marks_obtained','total_marks','timestamp',)

admin.site.register(QResponse,QResponseAdmin)
admin.site.register(PracticeResult,PracticeResultAdmin)
