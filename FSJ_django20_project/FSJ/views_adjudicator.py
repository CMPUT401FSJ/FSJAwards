from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import *
from .utils import *
from .filters import *
from .forms import *

# A test method to ensure a user is an Adjudicator to control access of certain views dependent on the user's class
def is_adjudicator(usr):
    user = get_FSJ_user(usr)
    if not isinstance(user, Adjudicator):
        raise PermissionDenied
    return True

# The user class specific home page handler, which returns the appropriate page for this user class.
# Contains the decordator to ensure the user is logged into the system and a test to ensure the user accessing the page is valid.
@login_required
@user_passes_test(is_adjudicator)
def adjudicator_home(request, FSJ_user):
    context = get_standard_context(FSJ_user)   
    template = loader.get_template("FSJ/home.html")
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_adjudicator)
def adjudicator_awards(request):
    FSJ_user = get_FSJ_user(request.user.username)
    awards_list = Award.objects.filter(committees__adjudicators = FSJ_user)
    filtered_list = AwardFilter(request.GET, queryset=awards_list)
    template = loader.get_template("FSJ/awards_list.html")
    context = get_standard_context(FSJ_user)
    context["awards_list"] = awards_list
    context["filter"] = filtered_list
    return HttpResponse(template.render(context,request))


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_application_list(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    application_list = award.applications.filter(is_reviewed = True)

    context = get_standard_context(FSJ_user)
    context["application_list"] = application_list
    context["return_url"] = "/adj_awardslist/"
    context["award"] = award
    context["is_adj"] = True

    template = loader.get_template("FSJ/application_list.html")
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_add_comment(request, award_idnum, application_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    application = Application.objects.get(application_id = application_idnum)
    
    try:
        comment = Comment.objects.get(application = application, adjudicator = FSJ_user)
        return redirect('adj_editcomment', award_idnum = award_idnum, application_idnum = application_idnum)
        
    except Comment.DoesNotExist:
    
        if request.method == "POST":
            form = CommentRestrictedForm(request.POST)
            if form.is_valid():
                comment = form.save(commit = False)
                comment.application = application
                comment.adjudicator = FSJ_user
                comment.save()
                return redirect('adj_applicationlist', award_idnum = award_idnum)
        else:
            return redirect('adj_applicationlist', award_idnum = award_idnum)
    
    
@login_required
@user_passes_test(is_adjudicator)
def adjudicator_edit_comment(request, award_idnum, application_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    application = Application.objects.get(application_id = application_idnum)
    
    try:
        comment = Comment.objects.get(application = application, adjudicator = FSJ_user)
        
        if request.method == "POST":
            form = CommentRestrictedForm(request.POST, instance = comment)
            if form.is_valid():
                comment = form.save(commit = False)
                comment.application = application
                comment.adjudicator = FSJ_user
                comment.save()
                return redirect('adj_applicationlist', award_idnum = award_idnum)
        else:
            return redirect('adj_applicationlist', award_idnum = award_idnum)
        
    except Comment.DoesNotExist:
        
        return redirect('adj_applicationlist', award_idnum = award_idnum)    
        
        
@login_required
@user_passes_test(is_adjudicator)
def adjudicator_delete_comment(request, award_idnum, application_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    application = Application.objects.get(application_id = application_idnum)
    
    comment = Comment.objects.get(application = application, adjudicator = FSJ_user).delete()
    return redirect('adj_applicationlist', award_idnum = award_idnum)
        