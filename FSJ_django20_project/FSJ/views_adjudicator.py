# Contains all adjudicator-specific views

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
from datetime import timezone
import xlwt


# A test method to ensure a user is an Adjudicator to control access of certain views dependent on the user's class
def is_adjudicator(usr):
    user = get_FSJ_user(usr)
    if not isinstance(user, Adjudicator):
        raise PermissionDenied
    return True

# The user class specific home page handler, which returns the appropriate page for this user class.
# Contains the decorator to ensure the user is logged into the system and a test to ensure the user accessing the page is valid.
@login_required
@user_passes_test(is_adjudicator)
def adjudicator_home(request, FSJ_user):
    context = get_standard_context(FSJ_user)   
    template = loader.get_template("FSJ/home.html")
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_adjudicator)
def adjudicator_awards(request):
    """Adjudicator view for seeing a list of the awards to be reviewed, which passes a list of the adjudicator's
    committees to the template
    """
    FSJ_user = get_FSJ_user(request.user.username)
    committee_list = Committee.objects.filter(adjudicators = FSJ_user).order_by('committee_name')
    template = loader.get_template("FSJ/adj_awards_list.html")
    context = get_standard_context(FSJ_user)
    context["committee_list"] = committee_list
    context["return_url"] = "/awards/"
    return HttpResponse(template.render(context,request))


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_application_list(request):
    """Adjudicator view for seeing a list of the applications for an award, which passes a list of applcations to
    the template
    """
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    # ranking_list is a list of all the adjudicator's rankings for this award, which is retrieved to help sort the
    # applications by ranking

    application_list = award.applications.filter(is_archived = False).order_by('student__ccid')
    ranking_list = Ranking.objects.filter(award = award, adjudicator = FSJ_user).order_by('rank')
    
    sorted_application_list = []
    sorted_ranking_list = []

    # Ranked applications are sorted by rank and put at the beginning of the list
    for ranking in ranking_list:
        sorted_application_list.append(ranking.application)
        sorted_ranking_list.append(ranking.rank)

    # All other applications are appended after the ranked applications
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

@login_required
@user_passes_test(is_adjudicator)
def adjudicator_application_action(request):
    """View handles adjudicator POST requests from the application list when they want to mark an award as
    having been reviewed or needing review"""
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == 'POST':
        if "_adjreview" in request.POST:
            award.add_reviewed(FSJ_user)

        elif '_adjUnreview' in request.POST:
            award.delete_reviewed(FSJ_user)

    return redirect('/awards/')


@login_required
@user_passes_test(is_adjudicator)
def adjudicator_add_edit_comment_ranking(request):
    """View handles POST requests from adjudicator_view_application and creates or edits the comment and ranking
    for a specific application.
    """
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
    """This is an obsolete method from before the Ranking model was added, designed to allow editing of comments"""
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
    """View deletes an adjudicator's comment and ranking for a specific application"""
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
    """View which handles adjudicator viewing of applications"""
    
    application_id = request.GET.get("application_id", "")
    
    FSJ_user = get_FSJ_user(request.user.username)
    context = get_standard_context(FSJ_user)
    # Return_url specifies where the view is being accessed from
    return_url = request.GET.get("return", "")
    url_is_safe = is_safe_url(url=urllib.parse.unquote(return_url),
                              allowed_hosts=settings.ALLOWED_HOSTS,
                              require_https=request.is_secure(), )

    try:
        # Archived applications can only be viewed by coordinators and get redirected
        application = Application.objects.get(application_id=application_id)
        if application.is_archived:
            return redirect('/home/')
    except Application.DoesNotExist:
        messages.warning(request, _("This application does not exist"))

        if url_is_safe:
            return redirect(urllib.parse.unquote(return_url))


    # Adjudicators cannot post directly to the application
    if request.method == 'POST':
        raise PermissionDenied

    else:
        try:
            comment = Comment.objects.get(application=application, adjudicator=FSJ_user)
            form = CommentRestrictedForm(instance=comment, prefix="form")

            delete_url = "/awards/delete/?award_id=" + str(application.award.awardid) + "&application_id=" + str(application.application_id)
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

        # form is the Comment form
        context["form"] = form
        # form2 is the Ranking form
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

@login_required
@user_passes_test(is_adjudicator)
def adjudicator_export_committee(request, committee_id):
    """Function creates an Excel file for a committee which lists all of its awards, its adjudicators' reviews and
    the final review comment for each award

    committee_id -- the uuid of the committee to be exported
    """
    try:
        committee = Committee.objects.get(committeeid=committee_id)
    except:
        messages.warning(request, _("Committee does not exist"))
        return redirect('/awards/')

    # filename is the name of the committee stripped of all spaces and with the current date appended
    filename = str(committee.committee_name).replace(" ", "") + "-" + datetime.now(timezone.utc).strftime(
        "%Y-%m-%d")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.xls"'

    wb = xlwt.Workbook(encoding='utf-8')

    awards = committee.awards.all()

    if awards:
        # Each award gets a new sheet in the workbook
        for award in awards:
            sheet_name = str((award.name).replace(" ", ""))[:30]
            ws = wb.add_sheet(sheet_name)

            col_width = 256 * 20  # 30 characters wide

            try:
                ws.col(0).width = 256 * 30
                for i in range(1, 6):
                    ws.col(i).width = col_width
            except ValueError:
                pass

            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Étudiant', 'Programme', "Année d'études", 'GPA', 'Crédits', ]

            # Writes headers to the workbook
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            applications = award.applications.filter(is_archived = False).order_by('student__ccid')

            # Write a row for each adjudicator containing their ccid and the ccids of their top-ranked applications
            for application in applications:

                student = application.student

                row_num += 1
                row = (student.get_name(), str(student.program.code), str(student.year), student.gpa, student.credits)

                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

    else:
        ws = wb.add_sheet("Sheet1")

    wb.save(response)
    return response
