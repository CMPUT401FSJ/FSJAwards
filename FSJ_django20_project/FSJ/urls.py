from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_to_home'),
    path('login/', auth_views.LoginView.as_view(template_name="FSJ/login.html", redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('studentlist/', views.coordinator_studentlist, name = 'studentlist'),
    path('studentlist/add/', views.coordinator_addstudent, name = 'addstudent'),
    path('studentlist/delete/', views.coordinator_deletestudent, name = 'deletestudent'),
    path('studentlist/<str:usr_ccid>/', views.coordinator_studentdetail, name = 'studentdetail'),
    path('adjudicatorlist/', views.coordinator_adjudicatorlist, name = 'adjudicatorlist'),
    path('adjudicatorlist/add/', views.coordinator_addadjudicator, name = 'addadjudicator'),
    path('adjudicatorlist/delete/', views.coordinator_deleteadjudicator, name = 'deleteadjudicator'),
    path('adjudicatorlist/<str:usr_ccid>/', views.coordinator_adjudicatordetail, name = 'adjudicatordetail'),
    path('coord_awardslist/', views.awards, name='coord_awardslist'),
    path('coord_awardslist/add/', views.coordinator_add_awards, name = 'coord_addaward'),
    path('coord_awardslist/delete/', views.coordinator_awarddelete, name='coord_deleteaward'),
    path('coord_awardslist/<str:award_idnum>/', views.coordinator_awardedit, name = 'coord_awardedit'),
    path('coord_yearslist/', views.years, name='coord_yearslist'),
    path('coord_yearslist/add/', views.coordinator_addyearofstudy, name = 'coord_addyear'),
    path('coord_yearslist/delete/', views.coordinator_yeardelete, name='coord_deleteyear'),
    path('coord_yearslist/<str:year_name>/', views.coordinator_yearedit, name = 'coord_yearedit'),
    path('coord_committeeslist/', views.committees, name = 'coord_committeeslist'),
    path('coord_committeeslist/add/', views.coordinator_addcommittee, name = 'coord_addcommittee'),
    path('coord_committeeslist/delete/', views.coordinator_committeedelete, name='coord_deletecommittee'),
    path('coord_committeeslist/<str:committee_idnum>/', views.coordinator_committeeedit, name = 'coord_committeeedit'),
]