from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string

def index(request):
    data = {'title': 'Главная страница'}
    return render(request=request, template_name='weather/index.html', context=data)


def about(request):
    data = {'title': 'О проекте'}
    return render(request=request, template_name='weather/about.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Упс. Страница не найдена</h1>')