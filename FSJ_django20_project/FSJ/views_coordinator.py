from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from .models import *
from .utils import *
from .forms import *

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
    template = loader.get_template("FSJ/coord_student_list.html")
    context = get_standard_context(FSJ_user)
    context["student_list"] = student_list
    return HttpResponse(template.render(context, request)) 

# The handler used by the Coordinator class to produce a list of all adjudicators in the database, using the adjudicator_student_list template.
@login_required
@user_passes_test(is_coordinator)
def coordinator_adjudicatorlist(request):
    FSJ_user = get_FSJ_user(request.user.username)
    adjudicator_list = Adjudicator.objects.all()
    template = loader.get_template("FSJ/coord_adjudicator_list.html")
    context = get_standard_context(FSJ_user)
    context["adjudicator_list"] = adjudicator_list
    return HttpResponse(template.render(context, request)) 


# The handler used by the Coordinator class to show a specific student's profile in detail, using the generic profile temmplate and the unrestricted student model (with all fields editable).
@login_required
@user_passes_test(is_coordinator)
def coordinator_studentdetail(request, usr_ccid):
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        student = Student.objects.get(ccid = usr_ccid)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")

    # This is only true if the coordinator has just made edits to the student's profile.
    if request.method == "POST":
        # Load a form with the old instance and override relevant fields with the new info in the request
        form = StudentForm(request.POST, instance=student)
        # Check for validity of all fields before saving, invalid forms are rendered back into the template to show errors and allow correction.
        if form.is_valid():
            form.save()
            return redirect('studentlist')        
    else:
        # If no edits have been performed, load a form with the student's info
        form = StudentForm(instance=student)
        
    context = get_standard_context(FSJ_user)
    context["student"] = student
    context["form"] = form
    url = "/studentlist/" + student.ccid + "/"
    context["url"] = url
    template = loader.get_template("FSJ/profile.html")
    return HttpResponse(template.render(context, request))


# The handler used by the Coordinator class to show a specific adjudicator's profile in detail, using the generic profile temmplate and the unrestricted adjudicator model (with all fields editable).
@login_required
@user_passes_test(is_coordinator)
def coordinator_adjudicatordetail(request, usr_ccid):
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        adjudicator = Adjudicator.objects.get(ccid = usr_ccid)
    except Adjudicator.DoesNotExist:
        raise Http404("Adjudicator does not exist")
    
    # This is only true if the coordinator has just made edits to the adjudicator's profile.
    if request.method == "POST":
        # Load a form with the old instance and override relevant fields with the new info in the request
        form = AdjudicatorForm(request.POST, instance=adjudicator)
        # Check for validity of all fields before saving, invalid forms are rendered back into the template to show errors and allow correction.
        if form.is_valid():
            form.save()
            return redirect('adjudicatorlist')
    else:
        # If no edits have been performed, load a form with the adjudicator's info
        form = AdjudicatorForm(instance=adjudicator)
    context = get_standard_context(FSJ_user)
    context["adjudicator"] = adjudicator
    context["form"] = form
    url = "/adjudicatorlist/" + adjudicator.ccid + "/"
    context["url"] = url
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
            return redirect('studentlist')
    else:
        # If the coordinator hasn't entered information yet, create a blank student form
        form = StudentForm()
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = form
    url = "/studentlist/add/"
    context["url"] = url
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
            return redirect('adjudicatorlist')
    else:
        # If the coordinator hasn't entered information yet, create a blank adjudicator
        form = AdjudicatorForm()           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/profile.html")
    context["form"] = form
    url = "/adjudicatorlist/add/"
    context["url"] = url
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
    template = loader.get_template("FSJ/coord_awards_list.html")
    context = get_standard_context(FSJ_user)
    context["awards_list"] = awards_list
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
    template = loader.get_template("FSJ/award.html")
    return HttpResponse(template.render(context, request))

#Function for handling coordinator deleting an award
@login_required
@user_passes_test(is_coordinator)
def coordinator_awarddelete(request):

    if request.method == 'POST':
        awardid_list = request.POST.getlist('todelete')

        for itemid in awardid_list:
            Award.objects.get(awardid=itemid).delete()

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
    return HttpResponse(template.render(context, request))

#function for handling coordinator editing an award
@login_required
@user_passes_test(is_coordinator)
def coordinator_yearedit(request, year_name):
    FSJ_user = get_FSJ_user(request.user.username)
    try:
        yearofstudy = YearOfStudy.objects.get(year = year_name)
    except YearOfStudy.DoesNotExist:
        raise Http404("Year does not exist")

    if request.method == "POST":
        form = YearOfStudyForm(request.POST, instance=yearofstudy)
        if form.is_valid():
            form.save()
            return redirect('coord_yearslist')

    else:
        form = YearOfStudyForm(instance=yearofstudy)
    context = get_standard_context(FSJ_user)
    context["year"] = yearofstudy
    context["form"] = form
    url = "/coord_yearslist/" + str(yearofstudy.year) + "/"
    context["url"] = url
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

# This handler allows a Coordinator to add a new committee
@login_required
@user_passes_test(is_coordinator)
def coordinator_addcommittee(request):
    FSJ_user = get_FSJ_user(request.user.username)
    
    # If the coordinator has just saved their new adjudicator, check for form validity before saving. Invalid forms are put back into the template to show errors.
    if request.method == "POST":
        # Loads adjudicator form with the new information
        form = CommitteeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coord_committeeslist')
    else:
        # If the coordinator hasn't entered information yet, create a blank adjudicator
        form = CommitteeForm()           
    context = get_standard_context(FSJ_user)
    template = loader.get_template("FSJ/committee.html")
    context["form"] = form
    url = "coord_committeeslist/add/"
    context["url"] = url
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

    if request.method == "POST":
        form = CommitteeForm(request.POST, instance=committee)
        if form.is_valid():
            form.save()
            return redirect('coord_committeeslist')

    else:
        form = CommitteeForm(instance=committee)
    context = get_standard_context(FSJ_user)
    context["committee"] = committee
    context["form"] = form
    url = "/coord_committeeslist/" + str(committee.committeeid) + "/"
    context["url"] = url
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
