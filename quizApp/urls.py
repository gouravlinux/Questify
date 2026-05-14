from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("student-dashboard/", views.studentdashboard, name="studentdashboard"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("quiz-page/<int:quiz_id>", views.quizpage, name="quizpage"),
    path("result/", views.result_view, name="result"),
    path("my-results/", views.my_results, name="myresults"),
]
