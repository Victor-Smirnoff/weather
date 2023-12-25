from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path(route='login/', view=views.login_user, name='login'),
    path(route='logout/', view=views.logout_user, name='logout'),


]