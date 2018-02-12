from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .models import *

def is_student(user):
    if not isinstance(user, Student) and not isinstance(user, User):
        raise PermissionDenied
    return True

def redirect_to_home(request):
    return home(request)

@login_required
@user_passes_test(is_student)
def home(request):
    FSJ_user = get_FSJ_user(request.user.username)
    if isinstance(FSJ_user, Student):
        template = loader.get_template("FSJ/student_home.html") #should likely redirect to the student's main landing page versus having a student home?
        return HttpResponse(template.render(context, request))
    elif isinstance(FSJ_user, Coordinator):
        template = loader.get_template("FSJ/home.html") #should likely redirect here too
        return HttpResponse(template.render(context, request))
    elif isinstance(FSJ_user, Adjudicator):
        template = loader.get_template("FSJ/home.html") #should likely redirect here too
        return HttpResponse(template.render(context, request))
    else:
        raise PermissionDenied("User is not a student, coordinator, or adjudicator")
    
@login_required
def profile(request):
    FSJ_user = get_FSJ_user(request.user.username)
    context = get_standard_context()
    context['FSJ_user'] = FSJ_user
    template = loader.get_template("FSJ/profile.html")
    return HttpResponse(template.render(context, request))

def get_FSJ_user(usr):
    FSJ_user = None
    try:
        FSJ_user = Student.objects.get(username=usr)
    except Student.DoesNotExist:
        try:
            FSJ_user = Adjudicator.objects.get(username=usr)
        except Adjudicator.DoesNotExist:
            try:
                FSJ_user = Coordinator.objects.get(username=usr)
            except Coordinator.DoesNotExist:
                pass
    return FSJ_user

def get_standard_context():
    context = dict()
    context['FSJ_user'] = None
    return context

