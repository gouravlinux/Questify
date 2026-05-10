from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# Create your views here.
@login_required
def create_quiz_view(request):
    if request.method == "POST":
        title = request.POST.get("quiz_title")
        duration = request.POST.get('time_limit')
        # quiz code was auto-generated in our Model's save() method
        new_quiz = Quiz.objects.create(title=title, creator=request.user,time_limit = duration)
        # instead of going back to dashboard, go to 'add-questions'
        # we pass the ID so Django knows which quiz to add qns. to
        return redirect("add_questions", quiz_id=new_quiz.id)
    return render(request, "quizApp/create_quiz.html")


def home_redirect_view(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Instructor").exists():
            return redirect("instructor_dashboard")
        return redirect("student_dashboard")
    # if not logged in, redirect to login or show landing page
    return render(request, "quizApp/index.html")


@login_required
def add_questions_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == "POST":
        q_text = request.POST.get("question_text")
        q_type = request.POST.get("question_type")  # single or multiple
        # grab options 1-4
        opt1 = request.POST.get("opt1")
        opt2 = request.POST.get("opt2")
        opt3 = request.POST.get("opt3")
        opt4 = request.POST.get("opt4")

        correct = request.POST.get("correct_answers")  # eg. "1" or "1,3"

        Question.objects.create(
            quiz=quiz,
            text=q_text,
            q_type=q_type,
            option1=opt1,
            option2=opt2,
            option3=opt3,
            option4=opt4,
            correct_answer=correct,
        )
        # stay on same page or add more qns or go back
        if "finish" in request.POST:
            messages.success(
                request, f"Quiz '{quiz.title}' has been published successfully!"
            )
            return redirect("instructor_dashboard")
    return render(request, "quizApp/add_questions.html", {"quiz": quiz})


def register_view(request):
    if request.method == "POST":
        # Grad data from the form
        u_name = request.POST.get("username")
        u_pass = request.POST.get("password")
        u_email = request.POST.get("email")
        u_role = request.POST.get("role")  # Student or Instructor

        # create user in sqlite
        user = User.objects.create_user(username=u_name, password=u_pass, email=u_email)

        # placement logic : role-based access control
        # we put them in group so we can restrict permissions later
        group, created = Group.objects.get_or_create(name=u_role)
        user.groups.add(group)

        # log them in and redirect to home
        login(request, user)
        return redirect("home")

    # renders the page
    return render(request, "quizApp/register.html")


def login_view(request):
    error = None
    if request.method == "POST":
        u_name = request.POST.get("username")
        u_pass = request.POST.get("password")

        user = authenticate(request, username=u_name, password=u_pass)

        if user is not None:
            login(request, user)
            # check role and redirect
            if user.groups.filter(name="Instructor").exists():
                return redirect("instructor_dashboard")
            else:
                return redirect("student_dashboard")
        else:
            error = "Invalid Username or Password"
    return render(request, "quizApp/login.html", {"error": error})


@login_required
def instructor_dashboard(request):
    # check if user is actually an instructor
    if not request.user.groups.filter(name="Instructor").exists():
        raise PermissionDenied
    return render(request, "quizApp/instructor_dashboard.html")


@login_required
def student_dashboard(request):
    if request.method == "POST":
        code = request.POST.get("quiz_code")
        # find quiz with this unique 6-digit code
        quiz = Quiz.objects.filter(quiz_code=code).first()
        if quiz:
            # if found, send them to quiz taking page
            return redirect('take_quiz',quiz_id = quiz.id)
        else:
            messages.error(request, "Invalid Quiz Code. Please try again.")
    return render(request, "quizApp/student_dashboard.html")

@login_required
def take_quiz_view(request, quiz_id):
    # fetch quiz and all its related qns
    quiz = get_object_or_404(Quiz, id = quiz_id)
    questions = quiz.questions.all() # uses 'related_name' from Model
    return render(request, 'quizApp/take_quiz.html',{
        'quiz':quiz,
        'questions':questions
    })

@login_required
def submit_quiz_view(request, quiz_id):
    if request.method == "POST":
        quiz = Quiz.objects.get(id = quiz_id)
        questions = quiz.questions.all()
        score = 0

        for q in questions:
            selected_option = request.POST.get(f'q_{q.id}')

            if(selected_option == q.correct_answer):
                score += 1
        return render(request, 'quizApp/results.html',{
            'score':score,
            'total':questions.count(),
            'quiz':quiz
        })

