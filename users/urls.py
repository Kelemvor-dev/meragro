from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('userlogin/', views.accontView, name='userlogin'),
    path('edit-profile/', views.editUsuProfile, name='edit-profile'),
    path('update-profile/', views.editProfile_view, name='update-profile'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]