from django.contrib import admin

from .models import Quiz, Question, Result, StudentAnswer


class QuestionInline(admin.TabularInline):

    model = Question

    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):

    list_display = ("title", "code", "time_limit")

    inlines = [QuestionInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = ("user", "quiz", "score", "total", "submitted_at")

    list_filter = ("quiz",)

    search_fields = ("user__username", "quiz__title")

admin.site.register(StudentAnswer)