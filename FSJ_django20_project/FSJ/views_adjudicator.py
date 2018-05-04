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
    committee_list = Committee.objects.filter(adjudicators = FSJ_user)
    template = loader.get_template("FSJ/adj_awards_list.html")
    context = get_standard_context(FSJ_user)
    context["committee_list"] = committee_list
    context["return_url"] = "/adj_awardslist/"
    return HttpResponse(template.render(context,request))


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_application_list(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    application_list = award.applications.filter(is_archived = False)
    ranking_list = Ranking.objects.filter(award = award, adjudicator = FSJ_user).order_by('rank')
    
    sorted_application_list = []
    sorted_ranking_list = []
    
    for ranking in ranking_list:
        sorted_application_list.append(ranking.application)
        sorted_ranking_list.append(ranking.rank)
        
    for application in application_list:
        if application not in sorted_application_list:
            sorted_application_list.append(application)
            sorted_ranking_list.append('--')
    
    application_list = zip(sorted_application_list, sorted_ranking_list)

    context = get_standard_context(FSJ_user)
    context["application_list"] = application_list
    context["return_url"] = "/adj_awardslist/"
    context["award"] = award
    context["url"] = "/adj_awardslist/" + str(award_idnum) + "/applications/action/"

    template = loader.get_template("FSJ/application_list.html")
    return HttpResponse(template.render(context, request))

def adjudicator_application_action(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == 'POST':
        if "_adjreview" in request.POST:
            award.add_reviewed(FSJ_user)

    return redirect('/adj_awardslist/')


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_add_edit_comment_ranking(request, award_idnum, application_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    application = Application.objects.get(application_id = application_idnum)
    
    application.add_reviewed(FSJ_user)
    
    try:
        comment = Comment.objects.get(application = application, adjudicator = FSJ_user)
        
        if request.method == "POST":
            form = CommentRestrictedForm(request.POST,  prefix = "form", instance = comment)
            if form.is_valid():
                comment = form.save(commit = False)
                comment.application = application
                comment.adjudicator = FSJ_user
                comment.save()
        
    except Comment.DoesNotExist:
    
        if request.method == "POST":
            form = CommentRestrictedForm(request.POST,  prefix = "form")
            if form.is_valid():
                comment = form.save(commit = False)
                
                if comment.comment_text:
                    comment.application = application
                    comment.adjudicator = FSJ_user
                    comment.save()
        
    try:
        
        ranking = Ranking.objects.get(application = application, adjudicator = FSJ_user)
        
        if request.method == "POST":
            form2 = RankingRestrictedForm(FSJ_user, application.award, request.POST, instance = ranking, prefix = "form2")
            if form2.is_valid():
                ranking = form2.save(commit = False)
                ranking.application = application
                ranking.adjudicator = FSJ_user
                ranking.award = application.award
                ranking.save()
                
            else:
                ranking.delete()
                
            
    except Ranking.DoesNotExist:
    
        if request.method == "POST":
            form2 = RankingRestrictedForm(FSJ_user, application.award, request.POST, prefix = "form2")
            if form2.is_valid():
                ranking = form2.save(commit = False)
                ranking.application = application
                ranking.adjudicator = FSJ_user
                ranking.award = application.award
                ranking.save()
                 
            
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
    try:
        ranking = Ranking.objects.get(application = application, adjudicator = FSJ_user)
        ranking.delete()   
        
    except:
        pass
    
    return redirect('adj_applicationlist', award_idnum = award_idnum)
        