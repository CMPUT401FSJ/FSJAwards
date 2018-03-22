from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_to_home'),
    path('login/', auth_views.LoginView.as_view(template_name="FSJ/login.html", redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('studentlist/', views.coordinator_studentlist, name = 'studentlist'),
    path('studentlist/add/', views.coordinator_addstudent, name = 'addstudent'),
    path('studentlist/addmulti/', views.coordinator_upload_students, name = 'uploadstudent'),
    path('studentlist/delete/', views.coordinator_deletestudent, name = 'deletestudent'),
    path('studentlist/<str:usr_ccid>/', views.coordinator_studentdetail, name = 'studentdetail'),
    path('adjudicatorlist/', views.coordinator_adjudicatorlist, name = 'adjudicatorlist'),
    path('adjudicatorlist/add/', views.coordinator_addadjudicator, name = 'addadjudicator'),
    path('adjudicatorlist/delete/', views.coordinator_deleteadjudicator, name = 'deleteadjudicator'),
    path('adjudicatorlist/<str:usr_ccid>/', views.coordinator_adjudicatordetail, name = 'adjudicatordetail'),
    path('coord_awardslist/', views.awards, name='coord_awardslist'),
    path('coord_awardslist/add/', views.coordinator_add_awards, name = 'coord_addaward'),
    path('coord_awardslist/action/', views.coordinator_awardaction, name='coord_awardaction'),
    path('coord_awardslist/<str:award_idnum>/', views.coordinator_awardedit, name = 'coord_awardedit'),
    path('programs/list_programs/', views.list_programs, name='list_programs'),
    path('programs/add/', views.add_program, name='add_program'),
    path('programs/edit/<str:program_code>/', views.edit_program, name='edit_program'),
    path('programs/delete/', views.delete_programs, name='delete_programs'),
    path('coord_yearslist/', views.years, name='coord_yearslist'),
    path('coord_yearslist/add/', views.coordinator_addyearofstudy, name = 'coord_addyear'),
    path('coord_yearslist/delete/', views.coordinator_yeardelete, name='coord_deleteyear'),
    path('coord_yearslist/<str:year_name>/', views.coordinator_yearedit, name = 'coord_yearedit'),
    path('coord_committeeslist/', views.committees, name = 'coord_committeeslist'),
    path('coord_committeeslist/add/', views.coordinator_addcommittee, name = 'coord_addcommittee'),
    path('coord_committeeslist/delete/', views.coordinator_committeedelete, name='coord_deletecommittee'),
    path('coord_committeeslist/<str:committee_idnum>/', views.coordinator_committeeedit, name = 'coord_committeeedit'),
    path('coord_awardslist/<str:award_idnum>/applications/', views.coordinator_application_list, name = 'coord_applicationlist'),
    path('student_awardslist/', views.student_awardslist, name = 'student_awardslist'),
    path('student_awardslist/<str:award_idnum>/apply/', views.student_addapplication, name = 'student_addapplication'),
    path('student_awardslist/<str:award_idnum>/edit/', views.student_editapplication, name = 'student_editapplication'),
    path('student_awardslist/<str:award_idnum>/unsubmit/', views.student_unsubmitapplication, name = 'student_unsubmitapplication'),
    path('adj_awardslist/', views.adjudicator_awards, name = 'adj_awardslist'),
    path('adj_awardslist/<str:award_idnum>/applications/', views.adjudicator_application_list, name = 'adj_applicationlist'),
    path('adj_awardslist/<str:award_idnum>/<str:application_idnum>/add/', views.adjudicator_add_comment, name = 'adj_addcomment'),
    path('adj_awardslist/<str:award_idnum>/<str:application_idnum>/edit/', views.adjudicator_edit_comment, name = 'adj_editcomment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
