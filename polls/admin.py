from django.contrib import admin
from .models import Question,Choice
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display=('question_text','pub_date','was_publiced_recently')
    list_filter=['pub_date']
    search_fields=['question_text'] # 搜索框
    fieldsets=[
        (None,{'fields':["question_text"]}),
        ('Date information',{'fields':['pub_date']}),
    ]
    inlines = [ChoiceInline] 

admin.site.register(Question,QuestionAdmin)
# admin.site.register(Choice)