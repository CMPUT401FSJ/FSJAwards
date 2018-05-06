from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
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

# A test method to ensure a user is a Coordinator to control access of certain views dependent on the user's class
def is_coordinator(usr):
    user = get_FSJ_user(usr)
    if not isinstance(user, Coordinator):
        raise PermissionDenied
    return True

# The user class specific home page handler, which returns the appropriate page for this user class.
# Contains the decordator to ensure the user is logged into the system and a test to ensure the user accessing the page is valid.
@login_required
@user_passes_test(is_coordinator)
def coordinator_home(request, FSJ_user):
    context = get_standard_context(FSJ_user)   
    template = loader.get_template("FSJ/home.html")
    return HttpResponse(template.render(context, request))


# The handler used by the Coordinator class to produce a list of all students in the database, using the coord_student_list template.
@login_required
@user_passes_test(is_coordinator)
def coordinator_studentlist(request):
    FSJ_user = get_FSJ_user(request.user.username)
    student_list = Student.objects.all()
    filtered_list = StudentFilter(request.GET, queryset=student_list)
    template = loader.get_template("FSJ/coord_student_list.html")
    context = get_standard_context(FSJ_user)
    context["student_list"] = student_list
    context["filter"] = filtered_list
    return HttpResponse(template.render(context, request))

# The handler used by the Coordinator class to produce a list of all adjudicators in the database, using the adjudicator_student_list template.
@login_required
@user_passes_test(is_coordinator)
def coordinator_adjudicatorlist(request):
    FSJ_user = get_FSJ_user(request.user.username)
    adjudicator_list = Adjudicator.objects.all()
    filtered_list = AdjudicatorFilter(request.GET, queryset=adjudicator_list)
    template = loader.get_template("FSJ/coord_adjudicator_list.html")
    context = get_standard_context(FSJ_user)
    context["adjudicator_list"] = adjudicator_list
    context["filter"] = filtered_list
    return HttpResponse(template.render(context, request)) 


# The handler used by the Coordinator class to show a specific student's profile in detail, using the generic profile temmplate and the unrestricted student model (with all fields editable).
@login_required
@user_passes_test(is_coordinator)
def edit_student(request):
    student_ccid = request.GET.get("ccid","")
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        student = Student.objects.get(ccid = student_ccid)
    except Student.DoesNotExist:
        raise Http404(_("Student does not exist"))
    
    # load a form with the year info with editable fields
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit = False)
            student.save()
            return redirect('studentlist')
    else:
        form = StudentForm(instance=student)
    return_url = "/studentlist/"
        
    context = get_standard_context(FSJ_user)
    context["student"] = student
    context["form"] = form
    context["return_url"] = return_url
    template = loader.get_template("FSJ/profile.html")
    return HttpResponse(template.render(context, request))


# The handler used by the Coordinator class to show a specific adjudicator's profile in detail, using the generic profile temmplate and the unrestricted adjudicator model (with all fields editable).
@login_required
@user_passes_test(is_coordinator)
def edit_adjudicator(request):
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
            return redirect('adjudicatorlist')
    else:
        form = AdjudicatorForm(instance=adjudicator)
    return_url = "/adjudicatorlist/"
        
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
            #generate a random 32 character password that will be reset on registration
            user.set_password(get_random_string(length=32))
            user.save()
            return redirect('studentlist')
    else:
        # If the coordinator hasn't entered information yet, create a blank student form
        form = StudentForm()
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = form
    url = "/studentlist/add/"
    context["url"] = url
    context["return_url"] = "/studentlist/"
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
            return redirect('adjudicatorlist')
    else:
        # If the coordinator hasn't entered information yet, create a blank adjudicator
        form = AdjudicatorForm()           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = form
    url = "/adjudicatorlist/add/"
    context["url"] = url
    context["return_url"] = "/adjudicatorlist/"
    return HttpResponse(template.render(context, request))


# This handler deletes students after their profiles have been selected from a checklist
@login_required
@user_passes_test(is_coordinator)
def coordinator_deletestudent(request):

    if request.method == 'POST':
        id_list = request.POST.getlist('instance')

        for usr_ccid in id_list:
            Student.objects.get(ccid=usr_ccid).delete()

    return redirect('studentlist')

# This handler deletes adjudicators after their profiles have been selected from a checklist
@login_required
@user_passes_test(is_coordinator)
def coordinator_deleteadjudicator(request):

    if request.method == 'POST':
        id_list = request.POST.getlist('instance')

        for usr_ccid in id_list:
            Adjudicator.objects.get(ccid=usr_ccid).delete()

    return redirect('adjudicatorlist')

#function for handling coordinator viewing a list of awards
@login_required
@user_passes_test(is_coordinator)
def coordinator_awards(request, FSJ_user):
    awards_list = Award.objects.all()
    filtered_list = AwardFilter(request.GET, queryset=awards_list)
    template = loader.get_template("FSJ/awards_list.html")
    context = get_standard_context(FSJ_user)
    context["form"] = DateChangeForm()
    context["awards_list"] = awards_list
    context["filter"] = filtered_list
    context["return_url"] = "/coord_awardslist/"
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
            return redirect('coord_awardslist')
    else:
        form = AwardForm()

    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/award.html")
    context["form"] = form
    url = "/coord_awardslist/add/"
    context["url"] = url
    context["return_url"] = "/coord_awardslist/"
    return HttpResponse(template.render(context,request))

#function for handling coordinator editing an award
@login_required
@user_passes_test(is_coordinator)
def coordinator_awardedit(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == "POST":
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            return redirect('coord_awardslist')

    else:
        form = AwardForm(instance=award)
    context = get_standard_context(FSJ_user)
    context["award"] = award
    context["form"] = form
    url = "/coord_awardslist/" + str(award.awardid) + "/"
    context["url"] = url
    context["return_url"] = "/coord_awardslist/"
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
                for itemid in awardid_list:
                    award = Award.objects.get(awardid=itemid)
                    award.reset(form.cleaned_data['start_date'], form.cleaned_data['end_date'])
                    award.save()
                    

    return redirect('coord_awardslist')

#function for handling coordinator viewing a list of programs
@login_required
@user_passes_test(is_coordinator)
def list_programs(request):
    FSJ_user = get_FSJ_user(request.user.username)
    programs_list = Program.objects.all()
    template = loader.get_template("FSJ/list_programs.html")
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
            return redirect('list_programs')
    else:
        form = ProgramForm()
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/program.html")
    context["form"] = form
    url = "/programs/add/"
    context["url"] = url
    context["return_url"] = "/programs/list_programs"
    return HttpResponse(template.render(context, request))

#function for handling coordinator editing a program
@login_required
@user_passes_test(is_coordinator)
def edit_program(request, program_code):
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        program = Program.objects.get(code = program_code)
    except Program.DoesNotExist:
        raise Http404("Program does not exist")

    if request.method == "POST":
        form = ProgramForm(request.POST, instance = program)
        if form.is_valid():
            form.save()
            return redirect('list_programs')
    else:
        form = ProgramForm(instance = program)
    context = get_standard_context(FSJ_user)
    context["program_code"] = program_code
    context["form"] = form
    url = "/programs/edit/" + str(program.code) + "/"
    context["url"] = url
    context["return_url"] = "/programs/list_programs/"
    template = loader.get_template("FSJ/program.html")
    return HttpResponse(template.render(context, request))

#Function for handling coordinator deleting one or more programs
@login_required
@user_passes_test(is_coordinator)
def delete_programs(request):
    if request.method == 'POST':
        program_code_list = request.POST.getlist('todelete')

        for item_code in program_code_list:
            Program.objects.get(code = item_code).delete()
    return redirect('list_programs')

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
            return redirect('coord_yearslist')
    else:
        # If the coordinator hasn't entered information yet, create a blank adjudicator
        form = YearOfStudyForm()           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/year_of_study.html")
    context["form"] = form
    url = "/coord_yearslist/add/"
    context["url"] = url
    context["return_url"] = "/coord_yearslist/"
    return HttpResponse(template.render(context, request))

#function for handling coordinator editing an award
@login_required
@user_passes_test(is_coordinator)
def edit_year(request):
    year_name = request.GET.get("year","")
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        yearofstudy = YearOfStudy.objects.get(year = year_name)
    except YearOfStudy.DoesNotExist:
        raise Http404(_("Year does not exist"))
    
    # load a form with the year info with editable fields
    if request.method == 'POST':
        form = YearOfStudyForm(request.POST, instance=yearofstudy)
        if form.is_valid():
            form.save()
            return redirect('coord_yearslist')
    else:
        form = YearOfStudyForm(instance=yearofstudy)
    return_url = "/coord_yearslist/"
        
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
        yearname_list = request.POST.getlist('todelete')

        for yearname in yearname_list:
            YearOfStudy.objects.get(year=yearname).delete()

    return redirect('coord_yearslist')

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
    available_awards = Award.objects.exclude(awardid__in = awards_blocked).values_list('awardid','award_name')
    # If the coordinator has just saved their new comittee, check for form validity before saving. Invalid forms are put back into the template to show errors.
    if request.method == "POST":
        # Loads adjudicator form with the new information
        form = CommitteeForm(available_awards, request.POST)
        if form.is_valid():
            form.save()
            return redirect('coord_committeeslist')
    else:
        # If the coordinator hasn't entered information yet, create a blank committee
        form = CommitteeForm(available_awards)           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/committee.html")
    context["form"] = form
    url = "/coord_committeeslist/add/"
    context["url"] = url
    context["return_url"] = "/coord_committeeslist/"
    return HttpResponse(template.render(context, request))

#function for handling coordinator editing a committee
@login_required
@user_passes_test(is_coordinator)
def coordinator_committeeedit(request, committee_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        committee = Committee.objects.get(committeeid = committee_idnum)
    except Committee.DoesNotExist:
        raise Http404("Committee does not exist")

    committees = Committee.objects.exclude(committeeid = committee.committeeid)
    awards_list = Award.objects.all()
    awards_blocked = []
    for instance in committees:
        for award in instance.awards.all():
            if award in awards_list:
                awards_blocked.append(award.awardid)
    available_awards = Award.objects.exclude(awardid__in = awards_blocked).values_list('awardid','award_name')
    selectedawards = committee.awards.all()

    if request.method == "POST":
        form = CommitteeForm(available_awards, request.POST, instance=committee)
        if form.is_valid():
            form.save()
            return redirect('coord_committeeslist')

    else:
        form = CommitteeForm(available_awards,instance=committee)
    context = get_standard_context(FSJ_user)
    context["committee"] = committee
    context["form"] = form
    url = "/coord_committeeslist/" + str(committee.committeeid) + "/"
    context["url"] = url
    context["return_url"] = "/coord_committeeslist/"
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

    return redirect('coord_committeeslist')

# Handler for coordinator to see applications
@login_required
@user_passes_test(is_coordinator)
def coordinator_application_list(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    
    try:
        award = Award.objects.get(awardid = award_idnum)

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
    context["return_url"] = "/coord_awardslist/"
    context["award"] = award
    context["url"] = "/coord_awardslist/" + str(award_idnum) + "/applications/action/"

    template = loader.get_template("FSJ/application_list.html")
    return HttpResponse(template.render(context, request))
    
#Handler used to produce the list of archived applications for an award using coord_application_archive template
@login_required
@user_passes_test(is_coordinator)
def coordinator_application_archive_list(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)

    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    archived_application_list = award.applications.filter(is_archived = True)


    context = get_standard_context(FSJ_user)
    context["archived_list"] = archived_application_list
    context["award"] = award
    context["return_url"] = "/coord_awardslist/" + str(award_idnum) + "/applications/"

    template = loader.get_template("FSJ/coord_application_archive.html") 
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_coordinator)
def coordinator_archived_application_view(request, award_idnum, application_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")
    try:
        application = Application.objects.get(application_id = application_idnum)
    except Award.DoesNotExist:
        raise Http404("application does not exist")

    context = get_standard_context(FSJ_user)
    context["student"] = application.student
    context["award"] = award
    context["application"] = application
    if application.application_file:
        context["document"] = settings.MEDIA_URL + str(application.application_file)    
    context["archived"] = True
    context["return_url"] = "/coord_awardslist/" + str(award_idnum) + "/applications/archive/"
    
    comment_list = Comment.objects.filter(application = application)
    
    if comment_list.count() > 0:
        ranking_list = []
        for comment in comment_list:
            try:
                ranking = Ranking.objects.get(application = application, adjudicator = comment.adjudicator)
                ranking_list.append(ranking.rank)
                
            except Ranking.DoesNotExist:
                ranking_list.append("--")
                
        comment_list = zip(comment_list, ranking_list)
        
        context["comment_list"] = comment_list    

    template = loader.get_template("FSJ/view_application.html")
    return HttpResponse(template.render(context, request))

#Function used to archive an application by createing a new archivedapp object and deleteing the old application.
#Also used to delete applications
@login_required
@user_passes_test(is_coordinator)
def coordinator_application_action(request, award_idnum):
    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == 'POST':
        application_list = request.POST.getlist('applicationaction')

        if "_archive" in request.POST:  
            for applicationid in application_list:
                application = Application.objects.get(application_id=applicationid)
                application.is_archived = True;
                application.save()
        elif "_review" in request.POST:
            for applicationid in application_list:
                application = Application.objects.get(application_id=applicationid)
                application.is_reviewed = True;
                application.save()
        elif "_delete" in request.POST:
            for applicationid in application_list:
                Application.objects.get(application_id=applicationid).delete()


    return redirect('/coord_awardslist/'+ str(award_idnum) +'/applications/')

#Function used to dearchive an archived application by createing a new application object and deleteing the old archived application.
#Also used to delete archived applications
@login_required
@user_passes_test(is_coordinator)
def coordinator_archive_action(request, award_idnum):
    try:
        award = Award.objects.get(awardid = award_idnum)
    except Award.DoesNotExist:
        raise Http404("Award does not exist")

    if request.method == 'POST':
        archived_application_list = request.POST.getlist('archiveaction')

        if "_removeFromArchive" in request.POST:  
            for applicationid in archived_application_list:
                archivedapp = Application.objects.get(application_id=applicationid)
                archivedapp.is_archived = False;
                archivedapp.save()
        elif "_delete" in request.POST:
            for applicationid in archived_application_list:
                ArchivedApplication.objects.get(application_id=applicationid).delete()


    return redirect('/coord_awardslist/'+ str(award_idnum) +'/applications/archive/')

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
                            ccid = row['CCID'],
                            defaults={'student_id': row['ID'], 'first_name': row['First Name'], 'last_name': row['Last Name'], 'email' : row['Email (Univ)'],
                                      'program' : program, 'year' : year, 'middle_name' : row['Middle Name'],},
                        ) 
                        
                if 'gpa_file' in request.FILES:
                    csv_file = request.FILES['gpa_file']
                    csv_file.seek(0)
                    gpareader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8-sig')))    
                    for row in gpareader:
                        student = Student.objects.get(ccid = row['CCID'])
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
    url = "/studentlist/addmulti/"
    context["url"] = url
    return HttpResponse(template.render(context, request))    
