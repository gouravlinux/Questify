from django.contrib import admin
from .models import Quiz, Question
# Register your models here.

# this class makes quiz codes visible in the list
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title','quiz_code','creator','created_at')
    readonly_fields = ('quiz_code',) # as it is auto-generated, make it read-only

# This allows to see questions inside the quiz admin page
class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 1

class QuizWithQuestionsAdmin(QuizAdmin):
    inlines = [QuestionInLine] 

# registering the models
admin.site.register(Quiz, QuizWithQuestionsAdmin)
admin.site.register(Question)