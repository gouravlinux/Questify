from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    # unique 6-digit code of quiz
    quiz_code = models.CharField(max_length=6,unique=True,editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        if not self.quiz_code:
            # if quiz code not made till now: make it
            self.quiz_code = str(uuid.uuid4()).upper()[:6]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    TYPE_CHOICES = [
        ('SINGLE','Single Correct'),
        ('MULTIPLE','Multiple Correct'),
    ]
    quiz = models.ForeignKey(Quiz, related_name='questions',on_delete=models.CASCADE)
    text = models.TextField()
    q_type = models.CharField(max_length=10,choices=TYPE_CHOICES,default='SINGLE')

    # Options
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)

    # correct answers are stored as strings like "1" or "1,3"
    correct_answer = models.CharField(max_length=10)

    def __str__(self):
        return self.text