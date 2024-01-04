from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path(route='login/', view=views.LoginUser.as_view(), name='login'),
    path(route='logout/', view=LogoutView.as_view(), name='logout'),
    path(route='register/', view=views.RegisterUser.as_view(), name='register'),
    path(route='profile/', view=views.ProfileUser.as_view(), name='profile'),

]