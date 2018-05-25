from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.utils.http import is_safe_url
from django.http import HttpResponse, Http404
from django.template import loader
from django.conf import settings
from django.shortcuts import redirect
from datetime import datetime, timezone
from django.contrib import messages
from .filters import *
from .models import *
from .utils import *
from .forms import *
import csv
import io
import xlwt
import urllib

# A test method to ensure a user is a Coordinator to control access of certain views dependent on the user's class
def is_coordinator(usr):
    user = get_FSJ_user(usr)
    if not isinstance(user, Coordinator):
        raise PermissionDenied
    return True

# The user class specific home page handler, which returns the appropriate page for this user class.
# Contains the decordator to ensure the user is logged into the system and a test to ensure the user accessing
# the page is valid.
@login_required
@user_passes_test(is_coordinator)
def coordinator_home(request, FSJ_user):
    context = get_standard_context(FSJ_user)   
    template = loader.get_template("FSJ/home.html")
    return HttpResponse(template.render(context, request))


# The handler used by the Coordinator class to produce a list of all students in the database, using the coord_student
# _list template.
@login_required
@user_passes_test(is_coordinator)
def coordinator_students(request):
    FSJ_user = get_FSJ_user(request.user.username)
    student_list = Student.objects.all().order_by('ccid')
    filtered_list = StudentFilter(request.GET, queryset=student_list)

    student_paginator = Paginator(filtered_list.qs, 25)

    template = loader.get_template("FSJ/coord_student_list.html")
    context = get_standard_context(FSJ_user)
    context["student_list"] = student_list

    page = request.GET.get('page', 1)

    try:
        students = student_paginator.page(page)
    except PageNotAnInteger:
        students = student_paginator.page(1)
    except EmptyPage:
        students = student_paginator.page(student_paginator.num_pages)

    context["filter"] = filtered_list
    context["students"] = students
    return HttpResponse(template.render(context, request))

# The handler used by the Coordinator class to produce a list of all adjudicators in the database,
# using the adjudicator_student_list template.
@login_required
@user_passes_test(is_coordinator)
def coordinator_adjudicators(request):
    FSJ_user = get_FSJ_user(request.user.username)
    adjudicator_list = Adjudicator.objects.all()
    filtered_list = AdjudicatorFilter(request.GET, queryset=adjudicator_list)
    template = loader.get_template("FSJ/coord_adjudicator_list.html")
    context = get_standard_context(FSJ_user)
    context["adjudicator_list"] = adjudicator_list
    context["filter"] = filtered_list
    return HttpResponse(template.render(context, request)) 


# The handler used by the Coordinator class to show a specific student's profile in detail,
# using the generic profile temmplate and the unrestricted student model (with all fields editable).
@login_required
@user_passes_test(is_coordinator)
def coordinator_edit_student(request):
    student_ccid = request.GET.get("ccid","")
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        student = Student.objects.get(ccid = student_ccid)
    except Student.DoesNotExist:
        raise Http404(_("Student does not exist"))
    
    # load a form with the year info with editable fields
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit = False)
            student.save()
            return redirect('/students/')
    else:
        form = StudentEditForm(instance=student)
    return_url = "/students/"
        
    context = get_standard_context(FSJ_user)
    context["student"] = student
    context["form"] = form
    context["return_url"] = return_url
    template = loader.get_template("FSJ/profile.html")
    return HttpResponse(template.render(context, request))


# The handler used by the Coordinator class to show a specific adjudicator's profile in detail,
# using the generic profile temmplate and the unrestricted adjudicator model (with all fields editable).
@login_required
@user_passes_test(is_coordinator)
def coordinator_edit_adjudicator(request):
    adjudicator_ccid = request.GET.get("ccid","")
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        adjudicator = Adjudicator.objects.get(ccid = adjudicator_ccid)
    except Adjudicator.DoesNotExist:
        raise Http404(_("Adjudicator does not exist"))
    
    # load a form with the year info with editable fields
    if request.method == 'POST':
        form = AdjudicatorForm(request.POST, instance=adjudicator)
        if form.is_valid():
            adjudicator = form.save(commit = False)
            adjudicator.save()
            return redirect('/adjudicators/')
    else:
        form = AdjudicatorForm(instance=adjudicator)
    return_url = "/adjudicators/"
        
    context = get_standard_context(FSJ_user)
    context["adjudicator"] = adjudicator
    context["form"] = form
    context["return_url"] = return_url
    template = loader.get_template("FSJ/profile.html")
    return HttpResponse(template.render(context, request))

# This handler allows a Coordinator to add a new Student
@login_required
@user_passes_test(is_coordinator)
def coordinator_addstudent(request):
    FSJ_user = get_FSJ_user(request.user.username)
    
    # If the coordinator has posted their request to create a student, check if the form is valid. If yes, save it, if no, re-render the page to show errors.
    if request.method == "POST":
        # Loads student form with the information given
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            data= form.cleaned_data
            #set the user's email to that of the adjudicator
            user = User.objects.get(username=data['ccid'])
            user.email = data['email']
            # Generate a random 32 character password that will be reset on registration
            user.set_password(get_random_string(length=32))
            user.save()
            return redirect('/students/')
    else:
        # If the coordinator hasn't entered information yet, create a blank student form
        form = StudentForm()
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = form
    url = "/students/add/"
    context["url"] = url
    context["return_url"] = "/students/"
    return HttpResponse(template.render(context, request))


# This handler allows a Coordinator to add a new Adjudicator
@login_required 
@user_passes_test(is_coordinator)
def coordinator_addadjudicator(request):
    FSJ_user = get_FSJ_user(request.user.username)
    
    # If the coordinator has just saved their new adjudicator, check for form validity before saving. Invalid forms are put back into the template to show errors.
    if request.method == "POST":
        # Loads adjudicator form with the new information
        form = AdjudicatorForm(request.POST)
        if form.is_valid():
            form.save()
            data= form.cleaned_data
            user = User.objects.get(username=data['ccid'])
            user.email = data['email']
            user.set_password(get_random_string(length=32))
            user.save()
            return redirect('/adjudicators/')
    else:
        # If the coordinator hasn't entered information yet, create a blank adjudicator
        form = AdjudicatorForm()           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = form
    url = "/adjudicators/add/"
    context["url"] = url
    context["return_url"] = "/adjudicators/"
    return HttpResponse(template.render(context, request))


# This handler deletes students after their profiles have been selected from a checklist
@login_required
@user_passes_test(is_coordinator)
def coordinator_deletestudent(request):

    if request.method == 'POST':
        id_list = request.POST.getlist('instance')

        for usr_ccid in id_list:
            Student.objects.get(ccid=usr_ccid).delete()

    return redirect('/students/')

# This handler deletes adjudicators after their profiles have been selected from a checklist
@login_required
@user_passes_test(is_coordinator)
def coordinator_deleteadjudicator(request):

    if request.method == 'POST':
        id_list = request.POST.getlist('instance')

        for usr_ccid in id_list:
            Adjudicator.objects.get(ccid=usr_ccid).delete()

    return redirect('/adjudicators/')

#function for handling coordinator viewing a list of awards
@login_required
@user_passes_test(is_coordinator)
def coordinator_awards(request, FSJ_user):
    awards_list = Award.objects.all().order_by("name")
    filtered_list = AwardFilter(request.GET, queryset=awards_list)
    template = loader.get_template("FSJ/awards_list.html")
    context = get_standard_context(FSJ_user)
    context["form"] = DateChangeForm()
    context["awards_list"] = awards_list
    context["filter"] = filtered_list
    context["return_url"] = "/awards/"
    return HttpResponse(template.render(context,request))

#function for handling coordinator adding an award
@login_required
@user_passes_test(is_coordinator)
def coordinator_add_awards(request):
    FSJ_user = get_FSJ_user(request.user.username)
    if request.method == "POST":
        form = AwardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/awards/')
    else:
        form = AwardForm()

    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/award.html")
    context["form"] = form
    url = "/awards/add/"
    context["url"] = url
    context["return_url"] = "/awards/"
    return HttpResponse(template.render(context,request))

#function for handling coordinator editing an award
@login_required
@user_passes_test(is_coordinator)
def coordinator_awardedit(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get("award_id", "")
    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == "POST":
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            return redirect('/awards/')

    else:
        form = AwardForm(instance=award)
    context = get_standard_context(FSJ_user)
    context["award"] = award
    context["form"] = form
    url = "/awards/edit/?award_id=" + str(award.awardid)
    context["url"] = url
    context["return_url"] = "/awards/"
    template = loader.get_template("FSJ/award.html")
    return HttpResponse(template.render(context, request))

#Function for handling coordinator deleting, activating or deactivating an award
@login_required
@user_passes_test(is_coordinator)
def coordinator_awardaction(request):

    if request.method == 'POST':
        
        awardid_list = request.POST.getlist('awardaction')
        
        if '_delete' in request.POST: 
            
            for itemid in awardid_list:
                Award.objects.get(awardid=itemid).delete()
                
        elif '_activate' in request.POST: 
            for itemid in awardid_list:
                award = Award.objects.get(awardid=itemid)
                award.is_active = True
                award.save()
            
        elif '_deactivate' in request.POST:
            for itemid in awardid_list:
                award = Award.objects.get(awardid=itemid)
                award.is_active = False
                award.save()       
                
        elif '_reset' in request.POST:
            form = DateChangeForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                
                for itemid in awardid_list:
                    award = Award.objects.get(awardid=itemid)
                    award.reset(start_date, end_date)
                    award.save()
                
                if start_date or end_date:
                    messages.success(request, _("Awards reset and dates changed"))
                
                else:
                    messages.success(request, _("Awards reset"))
                
        elif '_changeDate' in request.POST:
            form = DateChangeForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                
                if start_date or end_date:
                    for itemid in awardid_list:
                        award = Award.objects.get(awardid=itemid)
                        award.change_date(start_date, end_date)
                        award.save()
                    
                    messages.success(request, _("Award dates changed"))            
                    
            
            else:
                messages.warning(request, _("The start date cannot be later than the end date"))
                    

    return redirect('/awards/')

#function for handling coordinator viewing a list of programs
@login_required
@user_passes_test(is_coordinator)
def programs(request):
    FSJ_user = get_FSJ_user(request.user.username)
    programs_list = Program.objects.all()
    template = loader.get_template("FSJ/coord_program_list.html")
    context = get_standard_context(FSJ_user)
    context["programs_list"] = programs_list
    return HttpResponse(template.render(context, request))

#function for handling coordinator adding a program
@login_required
@user_passes_test(is_coordinator)
def add_program(request):
    FSJ_user = get_FSJ_user(request.user.username)
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/programs/')
    else:
        form = ProgramForm()
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/program.html")
    context["form"] = form
    url = "/programs/add/"
    context["url"] = url
    context["return_url"] = "/programs/"
    return HttpResponse(template.render(context, request))

#function for handling coordinator editing a program
@login_required
@user_passes_test(is_coordinator)
def edit_program(request):
    FSJ_user = get_FSJ_user(request.user.username)
    program_id = request.GET.get("program_id","")
    try:
        program = Program.objects.get(id = program_id)
    except Program.DoesNotExist:
        raise Http404("Program does not exist")

    if request.method == "POST":
        form = ProgramForm(request.POST, instance = program)
        if form.is_valid():
            form.save()
            return redirect('/programs/')
    else:
        form = ProgramForm(instance = program)
    context = get_standard_context(FSJ_user)
    context["program_id"] = program_id
    context["form"] = form
    url = "/programs/edit/?program_id=" + str(program.id)
    context["url"] = url
    context["return_url"] = "/programs/"
    template = loader.get_template("FSJ/program.html")
    return HttpResponse(template.render(context, request))

#Function for handling coordinator deleting one or more programs
@login_required
@user_passes_test(is_coordinator)
def delete_programs(request):
    if request.method == 'POST':
        program_id_list = request.POST.getlist('todelete')

        for item_id in program_id_list:
            Program.objects.get(id = item_id).delete()
    return redirect('/programs/')

#function for handling coordinator viewing a list of years of study
@login_required
@user_passes_test(is_coordinator)
def coordinator_yearslist(request, FSJ_user):
    years_list = YearOfStudy.objects.all()
    template = loader.get_template("FSJ/coord_years_list.html")
    context = get_standard_context(FSJ_user)
    context["years_list"] = years_list
    return HttpResponse(template.render(context,request))

# This handler allows a Coordinator to add a new year of study
@login_required
@user_passes_test(is_coordinator)
def coordinator_addyearofstudy(request):
    FSJ_user = get_FSJ_user(request.user.username)
    
    # If the coordinator has just saved their new adjudicator, check for form validity before saving. Invalid forms are put back into the template to show errors.
    if request.method == "POST":
        # Loads adjudicator form with the new information
        form = YearOfStudyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/years/')
    else:
        # If the coordinator hasn't entered information yet, create a blank adjudicator
        form = YearOfStudyForm()           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/year_of_study.html")
    context["form"] = form
    url = "/years/add/"
    context["url"] = url
    context["return_url"] = "/years/"
    return HttpResponse(template.render(context, request))

#function for handling coordinator editing an award
@login_required
@user_passes_test(is_coordinator)
def edit_year(request):
    year_id = request.GET.get("year","")
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        yearofstudy = YearOfStudy.objects.get(id = year_id)
    except YearOfStudy.DoesNotExist:
        raise Http404(_("Year does not exist"))
    
    # load a form with the year info with editable fields
    if request.method == 'POST':
        form = YearOfStudyForm(request.POST, instance=yearofstudy)
        if form.is_valid():
            form.save()
            return redirect('/years/')
    else:
        form = YearOfStudyForm(instance=yearofstudy)
    return_url = "/years/"
        
    context = get_standard_context(FSJ_user)
    context["year"] = yearofstudy
    context["form"] = form
    context["return_url"] = return_url
    template = loader.get_template("FSJ/year_of_study.html")
    return HttpResponse(template.render(context, request)) 

#Function for handling coordinator deleting an award
@login_required
@user_passes_test(is_coordinator)
def coordinator_yeardelete(request):

    if request.method == 'POST':
        year_id_list = request.POST.getlist('todelete')

        for year_id in year_id_list:
            YearOfStudy.objects.get(id=year_id).delete()

    return redirect('/years/')

#function for handling coordinator viewing a list of committees
@login_required
@user_passes_test(is_coordinator)
def coordinator_committeeslist(request, FSJ_user):
    committees_list = Committee.objects.all()
    template = loader.get_template("FSJ/coord_committee_list.html")
    context = get_standard_context(FSJ_user)
    context["committees_list"] = committees_list
    return HttpResponse(template.render(context,request))

@login_required
@user_passes_test(is_coordinator)
def coordinator_addcommittee(request):
    FSJ_user = get_FSJ_user(request.user.username)

    committees = Committee.objects.all()
    awards_list = Award.objects.all()
    awards_blocked = []
    for committee in committees:
        for award in committee.awards.all():
            if award in awards_list:
                awards_blocked.append(award.awardid)
    available_awards = Award.objects.exclude(awardid__in = awards_blocked).values_list('awardid','name')
    # If the coordinator has just saved their new comittee, check for form validity before saving. Invalid forms are put back into the template to show errors.
    if request.method == "POST":
        # Loads adjudicator form with the new information
        form = CommitteeForm(available_awards, request.POST)
        if form.is_valid():
            form.save()
            return redirect('/committees/')
    else:
        # If the coordinator hasn't entered information yet, create a blank committee
        form = CommitteeForm(available_awards)           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/committee.html")
    context["form"] = form
    url = "/committees/add/"
    context["url"] = url
    context["return_url"] = "/committees/"
    return HttpResponse(template.render(context, request))

#function for handling coordinator editing a committee
@login_required
@user_passes_test(is_coordinator)
def coordinator_committeeedit(request):
    FSJ_user = get_FSJ_user(request.user.username)
    committee_id = request.GET.get('committee_id', '')
    try:
        committee = Committee.objects.get(committeeid = committee_id)
    except Committee.DoesNotExist:
        raise Http404("Committee does not exist")

    committees = Committee.objects.exclude(committeeid = committee.committeeid)
    awards_list = Award.objects.all()
    awards_blocked = []
    for instance in committees:
        for award in instance.awards.all():
            if award in awards_list:
                awards_blocked.append(award.awardid)
    available_awards = Award.objects.exclude(awardid__in = awards_blocked).values_list('awardid','name')
    selectedawards = committee.awards.all()

    if request.method == "POST":
        form = CommitteeForm(available_awards, request.POST, instance=committee)
        if form.is_valid():
            form.save()
            return redirect('/committees/')

    else:
        form = CommitteeForm(available_awards,instance=committee)
    context = get_standard_context(FSJ_user)
    context["committee"] = committee
    context["form"] = form
    url = "/committees/edit/?committee_id=" + str(committee.committeeid)
    context["url"] = url
    context["return_url"] = "/committees/"
    template = loader.get_template("FSJ/committee.html")
    return HttpResponse(template.render(context, request))

#Function for handling coordinator deleting a committee
@login_required
@user_passes_test(is_coordinator)
def coordinator_committeedelete(request):

    if request.method == 'POST':
        committeeid_list = request.POST.getlist('instance')

        for itemid in committeeid_list:
            Committee.objects.get(committeeid=itemid).delete()

    return redirect('/committees/')

# Handler for coordinator to see applications
@login_required
@user_passes_test(is_coordinator)
def coordinator_application_list(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)

    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    application_list = award.applications.filter(is_archived = False)

    #delete in-progress applications if deadline is past
    if datetime.now(timezone.utc) > award.end_date: 
        for application in application_list:
            if not application.is_submitted:
                application.delete()
        award.refresh_from_db()
        #refresh application list after any deletes, if this isn't here, application list will
        #not update correctly after deletion
        application_list = award.applications.all()

    ranking_list = []
    
    for application in application_list:
        ranking_list.append('--')
        
    application_list = zip(application_list, ranking_list)
    
    context = get_standard_context(FSJ_user)
    context["application_list"] = application_list
    context["return_url"] = "/awards/"
    context["award"] = award
    context["url"] = "/awards/applications/action/?award_id=" + str(award_id)

    template = loader.get_template("FSJ/application_list.html")
    return HttpResponse(template.render(context, request))
    
#Handler used to produce the list of archived applications for an award using coord_application_archive template
@login_required
@user_passes_test(is_coordinator)
def coordinator_application_archive_list(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')

    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    archived_application_list = award.applications.filter(is_archived = True)


    context = get_standard_context(FSJ_user)
    context["archived_list"] = archived_application_list
    context["award"] = award
    context["return_url"] = "/awards/applications/?award_id=" + str(award_id)

    template = loader.get_template("FSJ/coord_application_archive.html") 
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_coordinator)
def coordinator_archived_application_view(request):
    FSJ_user = get_FSJ_user(request.user.username)
    context = get_standard_context(FSJ_user)
    award_id = request.GET.get('award_id', '')
    application_id = request.GET.get('application_id', '')

    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")
    try:
        application = Application.objects.get(application_id = application_id)
    except Award.DoesNotExist:
        raise Http404("application does not exist")

    adjudicators = application.adjudicators.all()
    comment_list = []
    ranking_list = []

    if adjudicators.count() > 0:
        for adjudicator in adjudicators:
            try:
                comment = Comment.objects.get(application=application, adjudicator=adjudicator)
                comment_list.append(comment.comment_text)
            except:
                comment_list.append("")

            try:
                ranking = Ranking.objects.get(application=application, adjudicator=adjudicator)
                ranking_list.append(ranking.rank)

            except Ranking.DoesNotExist:
                ranking_list.append("--")

        review_list = zip(adjudicators.values_list('ccid', flat=True), comment_list, ranking_list)
        context["review_list"] = review_list

    context["student"] = application.student
    context["award"] = award
    context["application"] = application
    if application.application_file:
        context["document"] = settings.MEDIA_URL + str(application.application_file)    
    context["archived"] = True
    context["return_url"] = "/awards/applications/archive/?award_id=" + str(award_id)


    template = loader.get_template("FSJ/view_application.html")
    return HttpResponse(template.render(context, request))

#Function used to archive an application by createing a new archivedapp object and deleting the old application.
#Also used to delete applications
@login_required
@user_passes_test(is_coordinator)
def coordinator_application_action(request):
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == 'POST':
        application_list = request.POST.getlist('applicationaction')

        if "_archive" in request.POST:  
            for applicationid in application_list:
                application = Application.objects.get(application_id=applicationid)
                application.is_archived = True
                application.save()
        elif "_review" in request.POST:
            for applicationid in application_list:
                application = Application.objects.get(application_id=applicationid)
                application.is_reviewed = True
                application.save()
        elif "_delete" in request.POST:
            for applicationid in application_list:
                Application.objects.get(application_id=applicationid).delete()


    return redirect('/awards/applications/?award_id=' + str(award_id))

#Function used to dearchive an archived application by creating a new application object and deleteing the old archived application.
#Also used to delete archived applications
@login_required
@user_passes_test(is_coordinator)
def coordinator_archive_action(request):
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == 'POST':
        archived_application_list = request.POST.getlist('archiveaction')

        if "_removeFromArchive" in request.POST:  
            for applicationid in archived_application_list:
                archivedapp = Application.objects.get(application_id=applicationid)
                archivedapp.is_archived = False
                archivedapp.save()
        elif "_delete" in request.POST:
            for applicationid in archived_application_list:
                Application.objects.get(application_id=applicationid).delete()


    return redirect('/awards/applications/archive/?award_id='+ str(award_id))

@login_required
@user_passes_test(is_coordinator)
def coordinator_upload_students(request):
    FSJ_user = get_FSJ_user(request.user.username)

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():

            try:
                if 'student_file' in request.FILES:
                    csv_file = request.FILES['student_file']
                    csv_file.seek(0)
                    studentreader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8-sig')))    
                    for row in studentreader:
                        program = Program.objects.get(code = row['Prog'])
                        year = YearOfStudy.objects.get(year = row['Year'])
                        obj, created = Student.objects.update_or_create(
                            student_id = row['ID'],
                            defaults={'ccid' : row['CCID'], 'first_name': row['First Name'], 'last_name': row['Last Name'], 'email' : row['Email (Univ)'],
                                      'program' : program, 'year' : year, 'middle_name' : row['Middle Name'],},
                        ) 
                        
                if 'gpa_file' in request.FILES:
                    csv_file = request.FILES['gpa_file']
                    csv_file.seek(0)
                    gpareader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8-sig')))    
                    for row in gpareader:
                        student = Student.objects.get(student_id = row['ID'])
                        if row['GPA']:
                            student.gpa = row['GPA']
                            student.save()
                
                form = FileUploadForm()                    
                messages.success(request, _('Upload success!'))
            
            except UnicodeDecodeError:
                messages.warning(request, _('Please upload a UTF-8 encoded CSV file.'))
                
            except KeyError:
                messages.warning(request, _('Please make sure all column names match specified column names.'))     
                
            except Program.DoesNotExist:
                messages.warning(request, _("Please ensure all required programs have been added."))
                
            except YearOfStudy.DoesNotExist:
                messages.warning(request, _("Please ensure all required years of study have been added.")) 
                
            except Student.DoesNotExist:
                messages.warning(request, _("The student you are attempting to upload a GPA for does not exist."))
                
            except:
                messages.warning(request, _("Unexpected error. Please confirm file is in a valid format, and has all required columns/programs/years."))
                
            
    else:
        form = FileUploadForm()
    
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/coord_student_upload.html")
    context["form"] = form
    url = "/students/addmulti/"
    context["url"] = url
    return HttpResponse(template.render(context, request))    

@login_required
@user_passes_test(is_coordinator)
def coordinator_application_tab(request):
    FSJ_user = get_FSJ_user(request.user.username)
    application_list = Application.objects.all().order_by('student__ccid')
    filtered_list = ApplicationFilter(request.GET, queryset=application_list)

    application_paginator = Paginator(filtered_list.qs, 25)

    page = request.GET.get('page', 1)

    try:
        applications = application_paginator.page(page)
    except PageNotAnInteger:
        applications = application_paginator.page(1)
    except EmptyPage:
        applications = application_paginator.page(application_paginator.num_pages)


    template = loader.get_template("FSJ/coord_application_tab.html")
    context = get_standard_context(FSJ_user)
    context["application_list"] = application_list
    context["filter"] = filtered_list
    context['applications'] = applications
    context["return_url"] = "/applications/"
    context["url"] = "/applications/action/"
    return HttpResponse(template.render(context,request))    
    

@login_required
@user_passes_test(is_coordinator)
def coordinator_application_tab_action(request):
    if request.method == 'POST':
        application_list = request.POST.getlist('applicationaction')

        if "_archive" in request.POST:  
            for applicationid in application_list:
                application = Application.objects.get(application_id=applicationid)
                application.is_archived = True
                application.save()
        if "_removeFromArchive" in request.POST:  
            for applicationid in application_list:
                application = Application.objects.get(application_id=applicationid)
                application.is_archived = False
                application.save()        
        elif "_review" in request.POST:
            for applicationid in application_list:
                application = Application.objects.get(application_id=applicationid)
                application.is_reviewed = True
                application.save()
        elif "_delete" in request.POST:
            for applicationid in application_list:
                Application.objects.get(application_id=applicationid).delete() 
    
        return redirect('/applications/')


def coordinator_export_final_review(request, committee_id):
    try:
        committee = Committee.objects.get(committeeid=committee_id)
    except:
        messages.warning(request, _("Committee does not exist"))
        return redirect('/committees/')

    filename = str(committee.committee_name).replace(" ", "") + "-" + datetime.now(timezone.utc).strftime("%Y-%m-%d")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.xls"'

    wb = xlwt.Workbook(encoding='utf-8')

    adjudicators = committee.adjudicators.all()
    awards = committee.awards.all()

    if adjudicators and awards:
        for award in awards:
            sheet_name = str((award.name).replace(" ", ""))[:30]
            ws = wb.add_sheet(sheet_name)

            col_width = 256 * 20  # 20 characters wide

            try:
                for i in range(0, 6):
                    ws.col(i).width = col_width
            except ValueError:
                pass

            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Adjudicator', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5', ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            for adjudicator in adjudicators:

                row_num += 1
                row = [None] * 6
                row[0] = str(adjudicator.ccid)

                for i in range(1, 6):
                    try:
                        row[i] = str(Ranking.objects.get(award=award, adjudicator=adjudicator, rank=i).application.student)
                    except:
                        row[i] = ""

                row = tuple(row)
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            row_num += 2
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            ws.write(row_num, 0, "Final Comment:", font_style)

            font_style = xlwt.XFStyle()

            ws.write(row_num, 1, award.review_comment, font_style)

    else:
        ws = wb.add_sheet("Sheet1")

    wb.save(response)
    return response


def coordinator_committee_review(request, committee_id):

    FSJ_user = get_FSJ_user(request.user.username)
    context = get_standard_context(FSJ_user)
    try:
        committee = Committee.objects.get(committeeid=committee_id)
    except:
        messages.warning(request, _("Committee does not exist"))
        return redirect('/committees/')

    context['committee'] = committee
    context['return_url'] = "/committees/"
    context['url'] = "/committees/" + str(committee.committeeid) + "/review/"
    awards_list = committee.awards.all()

    if request.method == 'POST':
        for award in awards_list:
            form = AwardReviewCommentForm(request.POST, prefix = str(award.awardid), instance = award)
            if form.is_valid():
                form.save()

        return redirect('/committees/')

    formlist = []

    for award in awards_list:
        form = AwardReviewCommentForm(instance = award, prefix = str(award.awardid))
        #formlist.append(form)
        award.form = form

    context["formlist"] = formlist
    context['awards_list'] = awards_list


    template = loader.get_template("FSJ/coord_final_review.html")
    return HttpResponse(template.render(context, request))

 
@login_required
@user_passes_test(is_coordinator)
def coordinator_view_application(request):
    application_id = request.GET.get("application_id", "")
    FSJ_user = get_FSJ_user(request.user.username)
    context = get_standard_context(FSJ_user)
    return_url = request.GET.get("return", "")
    url_is_safe = is_safe_url(url=urllib.parse.unquote(return_url),
                              allowed_hosts=settings.ALLOWED_HOSTS,
                              require_https=request.is_secure(), )

    try:
        application = Application.objects.get(application_id=application_id)
    except Application.DoesNotExist:
        messages.warning(request, _("This application does not exist"))

        if url_is_safe:
            return redirect(urllib.parse.unquote(return_url))
        else:
            return redirect('/applications/')

    if request.method == 'POST':
        if '_review' in request.POST:
            if application.award.documents_needed and not application.application_file:
                messages.warning(request, _("This application is missing a document"))
                return redirect("/view_application/?application_id=" + str(
                    application.application_id) + "&return=" + urllib.parse.quote(return_url))
            else:
                application.is_reviewed = True
        elif '_unreview' in request.POST:
            application.is_reviewed = False

        application.save()

        if url_is_safe:
            return redirect(urllib.parse.unquote(return_url))
        else:
            return redirect('/applications/')

    else:
        adjudicators = application.adjudicators.all()
        comment_list = []
        ranking_list = []

        if adjudicators.count() > 0:
            for adjudicator in adjudicators:
                try:
                    comment = Comment.objects.get(application = application, adjudicator = adjudicator)
                    comment_list.append(comment.comment_text)
                except:
                    comment_list.append("")

                try:
                    ranking = Ranking.objects.get(application=application, adjudicator=adjudicator)
                    ranking_list.append(ranking.rank)

                except Ranking.DoesNotExist:
                    ranking_list.append("--")


            review_list = zip(adjudicators.values_list('ccid', flat=True), comment_list, ranking_list)
            context["review_list"] = review_list


        context["student"] = application.student
        if application.application_file:
            context["document"] = settings.MEDIA_URL + str(application.application_file)
        context["award"] = application.award

        url = "/view_application/?application_id=" + str(application.application_id) + "&return=" + urllib.parse.quote(
            return_url)
        context["url"] = url

        if url_is_safe and return_url:
            context["return_url"] = str(return_url)

        context["archived"] = False
        context["FSJ_user"] = FSJ_user
        template = loader.get_template("FSJ/view_application.html")

        application.add_viewed(FSJ_user)
        return HttpResponse(template.render(context, request))



def coordinator_export_master_review(request):

    filename = "MasterReview-" + datetime.now(timezone.utc).strftime(
        "%Y-%m-%d")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.xls"'

    wb = xlwt.Workbook(encoding='utf-8')

    committees = Committee.objects.all()

    if committees:
        for committee in Committee.objects.all():

            sheet_name = str((committee.committee_name).replace(" ", ""))[:30]
            ws = wb.add_sheet(sheet_name)

            col_width = 256 * 20  # 20 characters wide

            try:
                for i in range(0, 7):
                    ws.col(i).width = col_width
            except ValueError:
                pass

            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Award', 'Adjudicator', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5', ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)


            adjudicators = committee.adjudicators.all()
            awards = committee.awards.all()

            if adjudicators and awards:

                for award in awards:

                    row_num += 1

                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = xlwt.Style.colour_map['dark_green_ega']
                    font_style.pattern = pattern

                    row = [""] * 7
                    for col_num in range(7):
                        ws.write(row_num, col_num, row[i], font_style)


                    font_style = xlwt.XFStyle()
                    font_style.font.bold = True

                    row_num += 1
                    ws.write(row_num, 0, award.name, font_style)
                    row_num += 1

                    font_style = xlwt.XFStyle()

                    for adjudicator in adjudicators:

                        row_num += 1
                        row = [None] * 7
                        row[1] = str(adjudicator.ccid)

                        for i in range(2, 7):
                            try:
                                row[i] = str(
                                    Ranking.objects.get(award=award, adjudicator=adjudicator, rank=i).application.student)
                            except:
                                row[i] = ""

                        row = tuple(row)
                        for col_num in range(len(row)):
                            ws.write(row_num, col_num, row[col_num], font_style)

                    row_num += 2
                    font_style = xlwt.XFStyle()
                    font_style.font.bold = True

                    ws.write(row_num, 0, "Final Comment:", font_style)

                    font_style = xlwt.XFStyle()

                    ws.write(row_num, 1, award.review_comment, font_style)


    else:
        ws = wb.add_sheet("Sheet1")

    wb.save(response)
    return response

