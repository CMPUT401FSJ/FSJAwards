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
    FSJ_user = get_FSJ_user(request.user.username)
    unfiltered_list = Award.objects.filter(Q(is_active = True), Q(years_of_study = FSJ_user.year), Q(programs = FSJ_user.program) | Q(programs__isnull = True))
   
    awards_list = []
    in_progress_list = []
    submitted_list = []
    
    for award in unfiltered_list:
        if award.is_open():
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
    FSJ_user = get_FSJ_user(request.user.username)
    now = datetime.now(timezone.utc)  
    
    awards_id_list = Application.objects.filter(Q(student = FSJ_user), Q(is_submitted = True)).values_list('award', flat=True)
    awards_list = Award.objects.filter(Q(pk__in=awards_id_list), Q(start_date__gt=now) | Q(end_date__lt=now))
    
    template = loader.get_template("FSJ/student_award_history.html")
    context = get_standard_context(FSJ_user)
    context["awards_list"] = awards_list    
    
    return HttpResponse(template.render(context,request))
    

@login_required
@user_passes_test(is_student)
def student_addapplication(request):
    FSJ_user = get_FSJ_user(request.user.username)
    award_id = request.GET.get('award_id', '')
    award = Award.objects.get(awardid = award_id)
    
    if not award.is_active:
        return redirect('/awards/')
    
    try:
        application = Application.objects.get(award = award, student = FSJ_user)
        return redirect('/awards/')
    
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
                    return redirect('/awards/')
                        
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
            
        else:
            form = ApplicationRestrictedForm()
    # If the student hasn't entered any information yet, create a new blank form
        context = get_standard_context(FSJ_user)
        template = loader.get_template("FSJ/student_apply.html")
        context["form"] = form
        context['award'] = award
        url = "awards/apply/?award_id=" + str(award.awardid)
        delete_url = "/awards/"
        context["url"] = url    
        context["delete_url"] = delete_url
        return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_student)
def student_editapplication(request):
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
            
        else:
            # If the student hasn't entered any information yet, create a new blank form
            form = ApplicationRestrictedForm(instance=application)
            
        context = get_standard_context(FSJ_user)
        template = loader.get_template("FSJ/student_apply.html")
        context["form"] = form
        context['award'] = award
        url = "/awards/edit/?award_id=" + str(award.awardid)
        delete_url = "/awards/delete/?award_id=" + str(award.awardid)
        context["url"] = url    
        context["delete_url"] = delete_url
        return HttpResponse(template.render(context, request))        

    except Application.DoesNotExist:    
        return redirect('/awards/')
     
    
@login_required
@user_passes_test(is_student)
def student_unsubmitapplication(request):
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

@login_required
@user_passes_test(is_student)
def student_deleteapplication(request):
    award_id = request.GET.get('award_id', '')
    
    if request.method == "POST":
        FSJ_user = get_FSJ_user(request.user.username)
        award = Award.objects.get(awardid = award_idn)
        try:
            application = Application.objects.get(award = award, student = FSJ_user)
            
            if (not award.is_active) or (not award.is_open()):
                return redirect('/awards/')
            else:
                application.delete()
            
        except:
            pass

    return redirect('/awards/')
    

