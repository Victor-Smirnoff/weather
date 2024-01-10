from django.urls import path
from . import views


urlpatterns = [
    path(route='', view=views.index, name='home'),
    path(route='about/', view=views.about, name='about'),
    path(route='search/', view=views.search, name='search'),
    path(route='save-error/', view=views.save_error, name='save_error'),

]