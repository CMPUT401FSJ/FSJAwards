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
def student_awardslist(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    unfiltered_list = Award.objects.filter(Q(is_active = True), Q(programs = FSJ_user.program) | Q(programs__isnull = True))
   
    awards_list = []
    in_progress_list = []
    submitted_list = []
    
    for award in unfiltered_list:
        try:
            application = Application.objects.get(award = award, student = FSJ_user.ccid)
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
def student_addapplication(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    award = Award.objects.get(awardid = award_idnum)
    
    if not award.is_active:
        return redirect('home')
    
    try:
        application = Application.objects.get(award = award, student = FSJ_user.ccid)
        return redirect('home')
    
    except Application.DoesNotExist:    
        if request.method == "POST":
            form = ApplicationRestrictedForm(request.POST, request.FILES)
            
            if form.is_valid():                    
                application = form.save(commit = False)
            
                if '_save' in request.POST: 
                    application.is_submitted = False  
                    application.student = FSJ_user
                    application.award = award
                    application.save()
                    return redirect('home')                    
                        
                elif '_submit' in request.POST:
                    if datetime.now(timezone.utc) > award.deadline:
                        return redirect('home')
                    application.is_submitted = True            
                    if award.documents_needed == True and not application.application_file:
                        messages.warning(request, 'Please upload a document.')
                    
                    else:
                        application.student = FSJ_user
                        application.award = award
                        application.save()
                        return redirect('home')
            
        else:
            form = ApplicationRestrictedForm()
    # If the student hasn't entered any information yet, create a new blank form
        context = get_standard_context(FSJ_user)
        template = loader.get_template("FSJ/student_apply.html")
        context["form"] = form
        context['award'] = award
        url = "/student_awardlist/" + award_idnum + "/apply/"
        context["url"] = url    
        return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_student)
def student_editapplication(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    award = Award.objects.get(awardid = award_idnum)
    
    if award.is_active == False:
        return redirect('home')
    
    try:
        application = Application.objects.get(award = award, student = FSJ_user.ccid)
        
        if application.is_submitted == True:
            return redirect('home')
        
        if request.method == "POST":
            form = ApplicationRestrictedForm(request.POST, request.FILES, instance = application)
            
            if form.is_valid():                    
                application = form.save(commit = False)
            
                if '_save' in request.POST: 
                    application.is_submitted = False
                    application.save()
                    return redirect('home')                    
                        
                elif '_submit' in request.POST:
                    application.is_submitted = True            
                    if award.documents_needed == True and not application.application_file:
                        messages.warning(request, 'Please upload a document.')
                    
                    else:
                        application.save()
                        return redirect('home')
            
        else:
            # If the student hasn't entered any information yet, create a new blank form
            form = ApplicationRestrictedForm(instance=application)
            
        context = get_standard_context(FSJ_user)
        template = loader.get_template("FSJ/student_apply.html")
        context["form"] = form
        context['award'] = award
        url = "/student_awardlist/" + award_idnum + "/edit/"
        context["url"] = url    
        return HttpResponse(template.render(context, request))        

    except Application.DoesNotExist:    
        return redirect('home')
     
    
@login_required
@user_passes_test(is_student)
def student_unsubmitapplication(request, award_idnum):
    FSJ_user = get_FSJ_user(request.user.username)
    award = Award.objects.get(awardid = award_idnum)    
    application = Application.objects.get(award = award, student = FSJ_user.ccid)
    application.is_submitted = False
    application.save()
    return redirect('home')



