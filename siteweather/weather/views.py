from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string
from weather.api_services.openweathermap_api import Weather_API_Service
from weather.forms import LocationForm
from weather.models import Locations


def index(request):
    context = {}
    context['title'] = 'Главная страница'

    if request.method == 'POST':
        if 'save' in request.POST:

            name = request.POST.get('name')
            latitude = float(request.POST.get('latitude').replace(',','.'))
            longitude = float(request.POST.get('longitude').replace(',','.'))
            user_id = request.user

            print(f"latitude={latitude}, longitude={longitude}, name={name}")

            # form = LocationForm(request.POST)
            # if form.is_valid():
            #     form.save()

            location = Locations.objects.create(name=name, latitude=latitude, longitude=longitude, user_id=user_id)
            location.save()



    return render(request=request, template_name='weather/index.html', context=context)


def about(request):
    context = {'title': 'О проекте'}
    return render(request=request, template_name='weather/about.html', context=context)


def search(request):
    context = {}
    context['title'] = 'Результаты поиска'

    form_data = request.POST
    city_name = form_data['city_name']
    context['city_name'] = city_name

    api_obj = Weather_API_Service()
    search_result = api_obj.find_by_city(cityname=city_name)
    context['search_result'] = search_result

    form = LocationForm()
    context['form'] = form

    return render(request=request, template_name='weather/search.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Упс. Страница не найдена</h1>')