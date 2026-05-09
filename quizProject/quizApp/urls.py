from django.urls import path 
from . import views

urlpatterns = [
    path('hello/',views.home_redirect_view, name = 'home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view, name = 'login'),
    path('instructor/',views.instructor_dashboard, name = "instructor_dashboard"),
    path('student/',views.student_dashboard, name = "student_dashboard"),
    path('create-quiz/',views.create_quiz_view, name='create_quiz'),
    path('add-questions/<int:quiz_id>/',views.add_questions_view,name="add_questions")
]