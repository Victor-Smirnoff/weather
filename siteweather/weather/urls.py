from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.WeatherHome.as_view(), name='home'),
    path(route='about/', view=views.AboutProject.as_view(), name='about'),
    path(route='search/', view=views.WeatherSearch.as_view(), name='search'),

]