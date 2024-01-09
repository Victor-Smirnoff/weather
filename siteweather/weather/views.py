from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string
from weather.api_services.openweathermap_api import Weather_API_Service



def index(request):
    data = {'title': 'Главная страница'}
    return render(request=request, template_name='weather/index.html', context=data)


def about(request):
    data = {'title': 'О проекте'}
    return render(request=request, template_name='weather/about.html', context=data)


def search(request):
    form_data = request.POST
    city_name = form_data['city_name']

    api_obj = Weather_API_Service()
    search_result = api_obj.find_by_city(cityname=city_name)

    data = {'title': 'Результаты поиска', 'city_name': city_name, 'search_result': search_result}
    return render(request=request, template_name='weather/search.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Упс. Страница не найдена</h1>')