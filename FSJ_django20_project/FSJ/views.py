from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import loader 
from .forms import *
from .models import *
from .utils import *
from .views_student import *
from .views_adjudicator import *
from .views_coordinator import *

# A method used to redirect users who have no path to bring them to their home page
def redirect_to_home(request):
    return home(request)

# The home page, split out depending on what class of user is requested.
# Contains the decordator to ensure the user is logged into the system.
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

# The profile view for the user accessing their own profile (with restricted field editting)
# Includes a POST handler for saving based on the results from the form, and adds the form back to the same template if validation fails
# Contains the decordator to ensure the user is logged into the system and a test to ensure the user accessing the page is valid.
@login_required
@user_passes_test(is_FSJ_user)
def profile(request):
    FSJ_user = get_FSJ_user(request.user.username)
    # Save the profile data if the request is a POST
    if request.method == "POST":
        if isinstance(FSJ_user, Student):
            profile_form = StudentRestrictedForm(request.POST, instance=FSJ_user)
        elif isinstance(FSJ_user, Adjudicator):
            profile_form = AdjudicatorRestrictedForm(request.POST, instance=FSJ_user)
        elif isinstance(FSJ_user, Coordinator):
            profile_form = CoordinatorRestrictedForm(request.POST, instance=FSJ_user)
        # If the from is valid, save it and redirect as a GET (POST, REDIRECT, GET).
        # If the form isn't valid we'll rerender it with the errors to display on the template
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

    else:
        # On a GET, we prefill the fields based on the instance of the user whose profile is being editted
        if isinstance(FSJ_user, Student):
            profile_form = StudentRestrictedForm(instance=FSJ_user)
        elif isinstance(FSJ_user, Adjudicator):
            profile_form = AdjudicatorRestrictedForm(instance=FSJ_user)
        elif isinstance(FSJ_user, Coordinator):
            profile_form = CoordinatorRestrictedForm(instance=FSJ_user)        
            
    # Add the form as well as this URL to the context, since the template is used for other handlers as well (for Coordinators to update other users' profiles)
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = profile_form
    url = "/profile/"
    context["url"] = url
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_coordinator)
def awards(request):
    FSJ_user = get_FSJ_user(request.user.username)
    return coordinator_awards(request, FSJ_user)

@login_required
@user_passes_test(is_coordinator)
def years(request):
    FSJ_user = get_FSJ_user(request.user.username)
    return coordinator_yearslist(request, FSJ_user)