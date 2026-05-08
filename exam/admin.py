from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Paper, Concept, QuestionType, Question


admin.site.register(Paper)
admin.site.register(Concept)
admin.site.register(QuestionType)



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "questiontype", "created_at",'concept','paper')