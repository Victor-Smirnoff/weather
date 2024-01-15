from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from weather.api_services.openweathermap_api import Weather_API_Service
from weather.forms import LocationForm
from weather.models import Locations
from weather.api_services.ISO_country_codes import countries
from django.views.generic import ListView, TemplateView
from django.core.cache import cache



class WeatherHome(ListView):
    template_name = 'weather/index.html'
    context_object_name = 'locations'
    extra_context = {}
    extra_context['title'] = 'Главная страница'
    form_class = LocationForm

    def get_queryset(self):
        locations = Locations.objects.filter(user_id=self.request.user.id).order_by('-id')
        api_obj = Weather_API_Service()
        locations_current_weather_dict = {}
        for location in locations:
            cache_key = 'locations_current_weather_' + str(location.id)
            location_current_weather = cache.get(cache_key)
            if location_current_weather:
                locations_current_weather_dict[location.id] = location_current_weather
            else:
                latitude = str(float(location.latitude))
                longitude = str(float(location.longitude))
                location_current_weather = api_obj.find_current_weather_by_coords(latitude, longitude)
                location_current_weather.city.name = location.name
                cache.set(cache_key, location_current_weather, 60*15)
                locations_current_weather_dict[location.id] = location_current_weather

        return locations_current_weather_dict

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if 'save' in request.POST:
                return self.post_save_handler(request)
            elif 'delete' in request.POST:
                return self.post_delete_handler(request)

    def post_save_handler(self, request):
        name = request.POST.get('name')
        latitude = float(request.POST.get('latitude').replace(',', '.'))
        longitude = float(request.POST.get('longitude').replace(',', '.'))
        user_id = request.user
        try:
            location = Locations.objects.create(name=name,
                                                latitude=latitude,
                                                longitude=longitude,
                                                user_id=user_id
                                                )
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

            return self.save_error(request)

    def post_delete_handler(self, request):
        location_id = request.POST.get('location_id')
        try:
            location = Locations.objects.get(id=location_id)
            cache_key = str(location.id)
            if cache.has_key(cache_key):
                try:
                    cache.delete(cache_key)
                except Exception as e:
                    print(f"Ошибка очистки кеша: {e}")
            location.delete()
            return redirect('home')
        except Exception:
            return redirect('home')

    def save_error(self, request):
        context = {}
        context['title'] = 'Ошибка добавления города'
        context['error_message'] = request.session.get('error_message')
        context['name'] = request.session.get('name')
        context['latitude'] = request.session.get('latitude')
        context['longitude'] = request.session.get('longitude')
        context['country'] = request.session.get('country')
        context['country_name'] = request.session.get('country_name')

        return render(request=request, template_name='weather/save_error.html', context=context)


class WeatherSearch(ListView):
    template_name = 'weather/search.html'
    extra_context = {}
    extra_context['title'] = 'Результаты поиска'
    form_class = LocationForm

    def post(self, request, *args, **kwargs):
        form_data = self.request.POST
        city_name = form_data['city_name']
        self.extra_context['city_name'] = city_name

        api_obj = Weather_API_Service()
        search_result = api_obj.find_by_city(cityname=city_name)
        self.extra_context['search_result'] = search_result

        return render(request=request, template_name='weather/search.html', context=self.extra_context)


class AboutProject(TemplateView):
    extra_context = {}
    extra_context['title'] = 'О проекте'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='weather/about.html', context=self.extra_context)


class WeatherForecast(TemplateView):
    extra_context = {}

    def post(self, request, location_id, *args, **kwargs):
        return self.render_page(request, location_id)

    def get(self, request, location_id, *args, **kwargs):
        locations = Locations.objects.filter(user_id=self.request.user.id).order_by('-id')
        lst_locations_id = [location.id for location in locations]
        if location_id not in lst_locations_id:
            raise Http404('Страница не найдена')
        else:
            return self.render_page(request, location_id)

    def render_page(self, request, location_id, *args, **kwargs):
        location = Locations.objects.get(id=location_id)
        self.extra_context['name'] = location.name
        self.extra_context['title'] = f'Прогноз погоды “{location.name}”'

        cache_key = 'locations_forecast_weather_' + str(location_id)
        forecast = cache.get(cache_key)
        if forecast:
            self.extra_context['forecast'] = forecast
            return render(request=request, template_name='weather/forecast.html', context=self.extra_context)
        else:
            latitude = float(str(location.latitude).replace(',', '.'))
            longitude = float(str(location.longitude).replace(',', '.'))
            api_obj = Weather_API_Service()
            forecast = api_obj.find_forecast_by_coords(latitude, longitude)
            self.extra_context['forecast'] = forecast
            cache.set(cache_key, forecast, 60 * 60)
            return render(request=request, template_name='weather/forecast.html', context=self.extra_context)


class PageNotFound404(TemplateView):
    extra_context = {}
    extra_context['title'] = 'Страница не найдена'

    def get(self, request, exception=None, *args, **kwargs):
        self.extra_context['path'] = request.path
        return render(request=request, template_name='404.html', status=404, context=self.extra_context)