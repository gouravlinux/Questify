from django.db import models
from django.contrib.auth.models import User
import random
import string


def generate_quiz_code():
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Quiz.objects.filter(code=code).exists():
            return code


# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(
        max_length=10, unique=True, blank=True, default=generate_quiz_code
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=10)  # in minutes

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    OPTION_CHOICES = [
        ("option1", "Option 1"),
        ("option2", "Option 2"),
        ("option3", "Option 3"),
        ("option4", "Option 4"),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=20, choices=OPTION_CHOICES)

    def __str__(self):
        return self.question


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','quiz')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

class StudentAnswer(models.Model):

    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_answer = models.CharField(
        max_length=20
    )

    correct_answer = models.CharField(
        max_length=20
    )



    def __str__(self):

        return (
            f"{self.result.user.username} - "
            f"{self.question.question}"
        )