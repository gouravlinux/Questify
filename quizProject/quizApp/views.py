from django.shortcuts import render, redirect
from .models import Quiz, Question, Result, StudentAnswer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):

    if request.method == "POST":

        code = request.POST.get("quiz_code").strip().upper()

        try:

            quiz = Quiz.objects.get(code=code)

            return redirect("quizpage", quiz_id=quiz.id)

        except Quiz.DoesNotExist:

            return render(request, "home.html", {"error": "Invalid quiz code"})

    return render(request, "home.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect("studentdashboard")

        return render(request, "login.html", {"error": "Invalid Credentials"})

    return render(request, "login.html")


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")

        email = request.POST.get("email")

        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            return render(
                request, "register.html", {"error": "Username already exists"}
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        login(request, user)

        return redirect("studentdashboard")

    return render(request, "register.html")


@login_required
def studentdashboard(request):

    return render(request, "studentdashboard.html")


@login_required
def quizpage(request, quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)

    already_attempted = Result.objects.filter(user=request.user, quiz=quiz).exists()

    if already_attempted:

        return render(request, "already_attempted.html", {"quiz": quiz})

    questions = quiz.questions.all()

    context = {
        "quiz": quiz,
        "questions": questions,
    }

    return render(request, "quizpage.html", context)


@login_required
def result_view(request):

    if request.method != "POST":

        return redirect("studentdashboard")

    quiz_id = request.POST.get("quiz_id")

    quiz = Quiz.objects.get(id=quiz_id)

    already_attempted = Result.objects.filter(user=request.user, quiz=quiz).exists()

    if already_attempted:

        return redirect("studentdashboard")

    questions = Question.objects.filter(quiz=quiz)

    score = 0

    total = questions.count()

    result = Result.objects.create(user=request.user, quiz=quiz, score=0, total=total)

    for q in questions:

        selected = request.POST.get(f"q{q.id}")

        if selected == q.correct_option:

            score += 1

        option_map = {
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
        }

        selected_text = option_map.get(selected, "Not Attempted")

        correct_text = option_map.get(q.correct_option, "Not Available")

        StudentAnswer.objects.create(
            result=result,
            question=q,
            selected_answer=selected_text,
            correct_answer=correct_text,
        )

    result.score = score

    result.save()

    context = {
        "score": score,
        "total": total,
        "quiz": quiz,
    }

    return render(request, "result.html", context)


@login_required
def leaderboard(request):

    results = Result.objects.order_by("-score", "submitted_at")

    context = {"results": results}

    return render(request, "leaderboard.html", context)


@login_required
def my_results(request):

    results = Result.objects.filter(user=request.user).order_by("-submitted_at")

    for result in results:

        answers = result.studentanswer_set.all()

        for ans in answers:

            option_map = {
                "option1": ans.question.option1,
                "option2": ans.question.option2,
                "option3": ans.question.option3,
                "option4": ans.question.option4,
            }

            ans.selected_text = option_map.get(ans.selected_answer, "Not Attempted")

            ans.correct_text = option_map.get(ans.correct_answer, "Not Available")

    context = {"results": results}

    return render(request, "my_results.html", context)


@login_required
def logout_view(request):

    logout(request)

    return redirect("home")
