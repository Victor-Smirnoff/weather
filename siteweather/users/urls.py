from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path(route='login/', view=views.LoginUser.as_view(), name='login'),
    path(route='logout/', view=LogoutView.as_view(), name='logout'),
    path(route='register/', view=views.RegisterUser.as_view(), name='register'),
    path(route='profile/', view=views.ProfileUser.as_view(), name='profile'),
    path(route='password-change/', view=views.UserPasswordChange.as_view(), name='password_change'),
    path(route='password-change/done/',
         view=PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'
    ),

]