from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from weather.api_services.openweathermap_api import Weather_API_Service
from weather.forms import LocationForm
from weather.models import Locations
from weather.api_services.ISO_country_codes import countries



def index(request):
    context = {}
    context['title'] = 'Главная страница'

    user_id = user_id = request.user.id
    locations = Locations.objects.filter(user_id=user_id).order_by('-id')

    api_obj = Weather_API_Service()
    locations_current_weather_dict = {}
    for location in locations:
        latitude = str(float(location.latitude))
        longitude = str(float(location.longitude))
        location_current_weather = api_obj.find_current_weather_by_coords(latitude, longitude)
        location_current_weather.city.name = location.name
        locations_current_weather_dict[location.id] = location_current_weather

    context['locations'] = locations_current_weather_dict

    if request.method == 'POST':
        if 'save' in request.POST:
            name = request.POST.get('name')
            latitude = float(request.POST.get('latitude').replace(',', '.'))
            longitude = float(request.POST.get('longitude').replace(',', '.'))
            user_id = request.user
            try:
                location = Locations.objects.create(name=name, latitude=latitude, longitude=longitude, user_id=user_id)
                location.save()
                return redirect('home')
            except Exception:
                request.session['error_message'] = f'Произошла ошибка: город “{name}” уже добавлен ранее'
                request.session['name'] = name
                request.session['latitude'] = latitude
                request.session['longitude'] = longitude
                country = request.POST.get('country')
                request.session['country'] = country
                request.session['country_name'] = countries[country]

                return redirect('save_error')

        elif 'delete' in request.POST:
            location_id = request.POST.get('location_id')
            try:
                location = Locations.objects.get(id=location_id)
                location.delete()
                return redirect('home')
            except Exception:
                return redirect('home')

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

def save_error(request):
    context = {}
    context['title'] = 'Ошибка добавления города'
    context['error_message'] = request.session.get('error_message')
    context['name'] = request.session.get('name')
    context['latitude'] = request.session.get('latitude')
    context['longitude'] = request.session.get('longitude')
    context['country'] = request.session.get('country')
    context['country_name'] = request.session.get('country_name')

    return render(request=request, template_name='weather/save_error.html', context=context)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Упс. Страница не найдена</h1>')