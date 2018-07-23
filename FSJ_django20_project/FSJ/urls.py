from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_to_home'),
    path('login/', auth_views.LoginView.as_view(template_name="FSJ/login.html", redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.registration, name='register'),
    path('register/password_set/(P<uidb64>[0-9A-Za-z]+)-(P<token>.+)/', views.register_activation, name='register_activation'),
    path('reset_password/', auth_views.password_reset, name='reset_password'),
    path('reset_password/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('reset_password/confirm/(P<uidb64>[0-9A-Za-z]+)-(P<token>.+)/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.password_reset_complete, name='password_reset_complete'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('students/', views.coordinator_students, name = 'students'),
    path('students/add/', views.coordinator_addstudent, name = 'addstudent'),
    path('students/addmulti/', views.coordinator_upload_students, name = 'uploadstudent'),
    path('students/delete/', views.coordinator_deletestudent, name = 'deletestudent'),
    path('students/edit/', views.coordinator_edit_student, name = 'coordinator_edit_student'),
    path('adjudicators/', views.coordinator_adjudicators, name = 'adjudicators'),
    path('adjudicators/add/', views.coordinator_addadjudicator, name = 'addadjudicator'),
    path('adjudicators/delete/', views.coordinator_deleteadjudicator, name = 'deleteadjudicator'),
    path('adjudicators/edit/', views.coordinator_edit_adjudicator, name = 'edit_adjudicator'),
    path('programs/', views.programs, name='programs'),
    path('programs/add/', views.add_program, name='add_program'),
    path('programs/edit/', views.edit_program, name='edit_program'),
    path('programs/delete/', views.delete_programs, name='delete_programs'),
    path('years/', views.years, name='years'),
    path('years/add/', views.coordinator_addyearofstudy, name = 'coord_addyear'),
    path('years/delete/', views.coordinator_yeardelete, name='coord_deleteyear'),
    path('years/edit/', views.edit_year, name = 'coord_edityear'),
    path('committees/', views.committees, name = 'committees'),
    path('committees/add/', views.coordinator_addcommittee, name = 'coord_addcommittee'),
    path('committees/delete/', views.coordinator_committeedelete, name='coord_deletecommittee'),
    path('committees/edit/', views.coordinator_committeeedit, name = 'coord_committeeedit'),
    path('awards/', views.awards, name='awards'),
    path('awards/add/', views.coordinator_add_awards, name = 'coord_addaward'),
    path('awards/action/', views.coordinator_awardaction, name='coord_awardaction'),
    path('awards/edit/', views.award_edit, name = 'award_edit'),    
    path('awards/applications/', views.award_applications, name = 'award_applications'),
    path('awards/applications/archive/view/', views.coordinator_archived_application_view, name = 'coord_applicationview'),
    path('awards/applications/archive/', views.coordinator_application_archive_list, name = 'coord_application_archive'),
    path('awards/applications/archive/action/', views.coordinator_archive_action, name = 'coord_archive_action'),
    path('awards/applications/action/', views.award_applications_action, name = 'application_action'),
    path('awards/apply/', views.student_addapplication, name = 'student_addapplication'),
    path('awards/unsubmit/', views.student_unsubmitapplication, name = 'student_unsubmitapplication'),
    path('awards/delete/', views.award_delete, name = 'award_application_delete'),
    path('history/', views.student_award_history, name = 'student_awardhistory'),
    path('view_student/', views.view_student, name = 'view_student'),
    path('view_application/', views.view_application, name = 'view_application'),
    path('applications/', views.coordinator_application_tab, name='coord_applicationtab'),
    path('applications/action/', views.coordinator_application_tab_action, name='coord_applicationtabaction'),
    re_path(r'^export/xls/master/$', views.coordinator_export_master_review, name='coordinator_export_master_review'),
    re_path(r'^export/xls/committee/(?P<committee_id>\S+)/$', views.coordinator_export_final_review, name='coordinator_export_final_review'),
    re_path(r'^committees/(?P<committee_id>\S+)/review/$', views.coordinator_committee_review, name='coord_committeereview'),
    re_path(r'^awards/export_committee/(?P<committee_id>\S+)/$', views.adjudicator_export_committee, name='adj_committee_export')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
