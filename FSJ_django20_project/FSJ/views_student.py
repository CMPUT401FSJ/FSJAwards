from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader
from .models import *
from .utils import *

# A test method to ensure a user is a Student to control access of certain views dependent on the user's class
def is_student(usr):
    user = get_FSJ_user(usr)
    if not isinstance(user, Student):
        raise PermissionDenied
    return True

# The user class specific home page handler, which returns the appropriate page for this user class.
# Contains the decordator to ensure the user is logged into the system and a test to ensure the user accessing the page is valid.
@login_required
@user_passes_test(is_student)
def student_home(request, FSJ_user):
    context = get_standard_context(FSJ_user)   
    template = loader.get_template("FSJ/student_home.html")
    return HttpResponse(template.render(context, request))