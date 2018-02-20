from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import loader
from .models import *
from .utils import *
from .views_student import *
from .views_adjudicator import *
from .views_coordinator import *

def redirect_to_home(request):
    return home(request)

@login_required
def home(request):
    FSJ_user = get_FSJ_user(request.user.username)
    if isinstance(FSJ_user, Student):
        return student_home(request, FSJ_user)
    elif isinstance(FSJ_user, Coordinator):
        return coordinator_home(request, FSJ_user)
    elif isinstance(FSJ_user, Adjudicator):
        return adjudicator_home(request, FSJ_user)
    else:
        raise PermissionDenied

@login_required
@user_passes_test(is_FSJ_user)
def profile(request):
    FSJ_user = get_FSJ_user(request.user.username)
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_coordinator)
def studentview(request):
    return coordinator_studentview(request)
