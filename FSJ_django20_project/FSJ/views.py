from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Student

def is_student(user):
    if not isinstance(user, Student) and not isinstance(user, User):
        raise PermissionDenied
    return True

def redirect_to_home(request):
    return home(request)

@login_required
@user_passes_test(is_student)
def home(request):
    student = get_student(request.user.username)
    if student:
        return render(request, "student_home.html")
    else:
        return render(request, "home.html")
    
@login_required
def profile(request):
    student = get_student(request.user.username)
    if student:
        return render(request, "student_profile.html", {"student" : student})
    return render(request, "profile.html")

def get_student(usr):
    try:
        student = Student.objects.get(username=usr)
    except Student.DoesNotExist:
        return None
    return student

