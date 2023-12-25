from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path(route='', view=views.index, name='home'),

]