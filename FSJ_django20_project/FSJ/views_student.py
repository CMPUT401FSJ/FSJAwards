# Contains all student-specific views

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.db.models import Q
from datetime import datetime, timezone
from .models import *
from .utils import *
from .forms import *


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

@login_required
@user_passes_test(is_student)
def student_awardslist(request):
    """Creates 3 lists of awards and sends them to the template so the student can apply for them or edit/unsubmit
    applications
    """
    FSJ_user = get_FSJ_user(request.user.username)

    # unfiltered_list contains all awards for which the student is eligible. The awards must match the student's
    # program and year of study and must be active awards.
    unfiltered_list = Award.objects.filter(Q(is_active = True), Q(years_of_study = FSJ_user.year) | Q(years_of_study__isnull = True),
                                           Q(programs = FSJ_user.program) | Q(programs__isnull = True)).order_by('name')

    # awards_list -- a list of awards the student hasn't applied for yet
    awards_list = []
    # in_progress_list -- a list of awards for which the student has saved but not submitted applications
    in_progress_list = []
    # submitted_list -- a list of awards for which the student has submitted applications
    submitted_list = []
    
    for award in unfiltered_list:

        # Checks if the current date is within the award's permitted date range
        if award.is_open():

            # sorts the unfiltered list into the three appropriate lists
            try:
                application = Application.objects.get(award = award, student = FSJ_user)
                if application.is_submitted:
                    submitted_list.append(award)
                elif not application.is_submitted:
                    in_progress_list.append(award)
            except Application.DoesNotExist:
                awards_list.append(award)
            
    template = loader.get_template("FSJ/student_awards_list.html")
    context = get_standard_context(FSJ_user)
    context["awards_list"] = awards_list
    context["in_progress_list"] = in_progress_list
    context["submitted_list"] = submitted_list
    return HttpResponse(template.render(context,request))

@login_required
@user_passes_test(is_student)
def student_award_history(request):
    """View displays a list of all awards which the student has applied for in the past cycle which are now closed"""
    FSJ_user = get_FSJ_user(request.user.username)
    now = datetime.now(timezone.utc)  

    # Gets the list of all awards the student has applications for
    awards_id_list = Application.objects.filter(Q(student = FSJ_user), Q(is_submitted = True)).values_list('award', flat=True)

    # Filters the list based on whether the award's start date is after today or its end date is before today
    awards_list = Award.objects.filter(Q(pk__in=awards_id_list), Q(start_date__gt=now) | Q(end_date__lt=now))
    
    template = loader.get_template("FSJ/student_award_history.html")
    context = get_standard_context(FSJ_user)
    context["awards_list"] = awards_list    
    
    return HttpResponse(template.render(context,request))
    

@login_required
@user_passes_test(is_student)
def student_addapplication(request):
    """View allowing a student to create a new application for a given award"""
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    award = Award.objects.get(awardid = award_id)

    # The award must be open
    if not award.is_active:
        return redirect('/awards/')

    # There cannot be two applications by the same student for the same award
    try:
        application = Application.objects.get(award = award, student = FSJ_user)
        return redirect('/awards/')
    
    except Application.DoesNotExist:    
        if request.method == "POST":
            form = ApplicationRestrictedForm(request.POST, request.FILES)
            
            if form.is_valid():                    
                application = form.save(commit = False)

                # If the application is being saved and not submitted, no need to check for application document
                if '_save' in request.POST: 
                    application.is_submitted = False  
                    application.student = FSJ_user
                    application.award = award
                    application.save()
                    return redirect('/awards/')

                # The application cannot be submitted without a document if it needs one
                elif '_submit' in request.POST:
                    if not award.is_open():
                        return redirect('/awards/')
                    if award.documents_needed == True and not application.application_file:
                        messages.warning(request, 'Please upload a document.')
                    
                    else:
                        application.is_submitted = True
                        application.student = FSJ_user
                        application.award = award
                        application.save()
                        return redirect('/awards/')

                # The student can cancel their application and be returned to the awards list
                elif '_delete' in request.POST:
                    return redirect('/awards/')
            
        else:
            form = ApplicationRestrictedForm()
    # If the student hasn't entered any information yet, create a new blank form
        context = get_standard_context(FSJ_user)
        template = loader.get_template("FSJ/student_apply.html")
        context["form"] = form
        context['award'] = award
        url = "awards/apply/?award_id=" + str(award.awardid)
        context["url"] = url
        return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_student)
def student_editapplication(request):
    """View allowing a student to edit and/or submit their saved application"""
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    
    
    try:
        award = Award.objects.get(awardid = award_id)
        application = Application.objects.get(award = award, student = FSJ_user)
        
        if (not application.award.is_active) or (not application.award.is_open()):
            return redirect('/awards/')
        
        if application.is_submitted:
            return redirect('/awards/')
        
        if request.method == "POST":
            form = ApplicationRestrictedForm(request.POST, request.FILES, instance = application)
            
            if form.is_valid():                    
                application = form.save(commit = False)
            
                if '_save' in request.POST: 
                    application.is_submitted = False
                    application.save()
                    return redirect('/awards/')
                        
                elif '_submit' in request.POST:
                    if not award.is_open():
                        return redirect('/awards/')
                    application.is_submitted = True            
                    if award.documents_needed == True and not application.application_file:
                        messages.warning(request, 'Please upload a document.')
                    
                    else:
                        application.save()
                        return redirect('/awards/')

                elif '_delete' in request.POST:
                    try:
                        application = Application.objects.get(award=award, student=FSJ_user)

                        if (not award.is_active) or (not award.is_open()):
                            return redirect('/awards/')
                        else:
                            application.delete()

                    except:
                        pass

                    return redirect('/awards/')
            
        else:
            form = ApplicationRestrictedForm(instance=application)
            
        context = get_standard_context(FSJ_user)
        template = loader.get_template("FSJ/student_apply.html")
        context["form"] = form
        context['award'] = award
        url = "/awards/edit/?award_id=" + str(award.awardid)
        context["url"] = url
        return HttpResponse(template.render(context, request))

    except Application.DoesNotExist:    
        return redirect('/awards/')
     
    
@login_required
@user_passes_test(is_student)
def student_unsubmitapplication(request):
    """View allowing a student to unsubmit their submitted application for further editing as long as the award
    is still active and open"""
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    
    try:
        award = Award.objects.get(awardid = award_id)
        
        if (not award.is_active) or (not award.is_open()):
            return redirect('/awards/')
        
        application = Application.objects.get(award = award, student = FSJ_user)
        application.is_submitted = False
        application.save()
        
    except:
        pass
    return redirect('/awards/')


    

