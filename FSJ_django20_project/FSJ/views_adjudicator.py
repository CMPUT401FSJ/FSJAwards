from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.utils.http import is_safe_url
from django.utils.translation import gettext_lazy as _
from .models import *
from .utils import *
from .filters import *
from .forms import *
import urllib

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
    context["return_url"] = "/awards/"
    return HttpResponse(template.render(context,request))


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_application_list(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)
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
    context["return_url"] = "/awards/"
    context["award"] = award
    context["url"] = "/awards/applications/action/?award_id=" + str(award_id)

    template = loader.get_template("FSJ/application_list.html")
    return HttpResponse(template.render(context, request))

def adjudicator_application_action(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == 'POST':
        if "_adjreview" in request.POST:
            award.add_reviewed(FSJ_user)

    return redirect('/awards/')


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_add_edit_comment_ranking(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    application_id = request.GET.get('application_id', '')
    
    
    application = Application.objects.get(application_id = application_id)
    
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
                 
            
    return redirect('/awards/applications/?award_id='+ str(award_id))
    
    
@login_required
@user_passes_test(is_adjudicator)
def adjudicator_edit_comment(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    application_id = request.GET.get('application_id', '')    
    
    application = Application.objects.get(application_id = application_id)
    
    try:
        comment = Comment.objects.get(application = application, adjudicator = FSJ_user)
        
        if request.method == "POST":
            form = CommentRestrictedForm(request.POST, instance = comment)
            if form.is_valid():
                comment = form.save(commit = False)
                comment.application = application
                comment.adjudicator = FSJ_user
                comment.save()
                return redirect('/awards/applications/?award_id='+ str(award_id))
        else:
            return redirect('/awards/applications/?award_id='+ str(award_id))
        
    except Comment.DoesNotExist:
        
        return redirect('/awards/applications/?award_id='+ str(award_id))    
        
        
@login_required
@user_passes_test(is_adjudicator)
def adjudicator_delete_comment(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    application_id = request.GET.get('application_id', '')    
    
    application = Application.objects.get(application_id = application_id)
    
    try:
        comment = Comment.objects.get(application = application, adjudicator = FSJ_user)
        ranking = Ranking.objects.get(application = application, adjudicator = FSJ_user)
        comment.delete()
        ranking.delete()   
        
    except:
        pass
    
    return redirect('/awards/applications/?award_id='+ str(award_id))

@login_required
@user_passes_test(is_adjudicator)
def adjudicator_view_application(request):
    
    application_id = request.GET.get("application_id", "")
    
    FSJ_user = get_FSJ_user(request.user.username)
    context = get_standard_context(FSJ_user)
    return_url = request.GET.get("return", "")
    url_is_safe = is_safe_url(url=urllib.parse.unquote(return_url),
                              allowed_hosts=settings.ALLOWED_HOSTS,
                              require_https=request.is_secure(), )

    try:
        application = Application.objects.get(application_id=application_id)
        if application.is_archived:
            return redirect('home')
    except Application.DoesNotExist:
        messages.warning(request, _("This application does not exist"))

        if url_is_safe:
            return redirect(urllib.parse.unquote(return_url))


    if request.method == 'POST':
        raise PermissionDenied

    else:
        try:
            comment = Comment.objects.get(application=application, adjudicator=FSJ_user)
            form = CommentRestrictedForm(instance=comment, prefix="form")

            delete_url = "/awards/delete/?awardid=" + str(application.award.awardid) + "&application_id=" + str(application.application_id)
            context["delete_url"] = delete_url

        except Comment.DoesNotExist:
            form = CommentRestrictedForm(prefix="form")

        try:
            ranking = Ranking.objects.get(application=application, adjudicator=FSJ_user)
            form2 = RankingRestrictedForm(FSJ_user, application.award, instance=ranking, prefix="form2")
            context["ranking"] = ranking

        except Ranking.DoesNotExist:
            form2 = RankingRestrictedForm(FSJ_user, application.award, prefix="form2")

        url = "/awards/edit/?award_id=" + str(application.award.awardid) + "&application_id=" + str(application.application_id)
        context["form"] = form
        context["form2"] = form2
        context["adjudicator"] = FSJ_user

        context["student"] = application.student
        if application.application_file:
            context["document"] = settings.MEDIA_URL + str(application.application_file)
        context["award"] = application.award
        context["url"] = url
        if url_is_safe and return_url:
            context["return_url"] = str(return_url)

        context["archived"] = False
        context["FSJ_user"] = FSJ_user
        template = loader.get_template("FSJ/view_application.html")

        application.add_viewed(FSJ_user)
        return HttpResponse(template.render(context, request))