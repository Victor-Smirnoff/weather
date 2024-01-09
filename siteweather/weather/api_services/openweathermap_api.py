import requests
from datetime import datetime
from ENV import API_KEY
from dto_response.city_response import CityResponse
from dto_response.error_response import ErrorResponse
from dto_response.current_weather_response import CurrentWeatherResponse
from dto_response.forecast_weather_response import ForecastWeatherResponse



class Weather_API_Service:
    """
    Класс для обращения к API сайта openweathermap.org
    """

    def find_by_city(self, cityname):
        """
        Метод возвращает либо список с найденными городами, либо объект класса ErrorResponse с кодом и описанием ошибки
        :param cityname: название города
        :return: список или объект ошибки ErrorResponse
        """
        limit = 5
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit={limit}&appid={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            if len(json_response) > 0:
                cities_list = []
                for res in json_response:
                    name = res['name']
                    lat = res['lat']
                    lon = res['lon']
                    country = res['country']
                    city_obj = CityResponse(name=name, lat=lat, lon=lon, country=country)
                    cities_list.append(city_obj)
                return cities_list
            else:
                error_obj = ErrorResponse(code=404, message=f'Город {cityname} не найден')
                return error_obj
        else:
            code = response.status_code
            message = f'Произошла ошибка при выполнении запроса: {code}'
            error_obj = ErrorResponse(code=code, message=message)
            return error_obj

    def find_current_weather_by_coords(self, lat, lon):
        """
        Метод находит текущую погоду в городе по координатам (широта и долгота)
        :param lat: широта
        :param lon: долгота
        :return: объект класса CurrentWeatherResponse
        """
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()

            name = json_response['name']
            lat = json_response['coord']['lat']
            lon = json_response['coord']['lon']
            country = json_response['sys']['country']
            city = CityResponse(name=name, lat=lat, lon=lon, country=country)

            weather_desc = json_response['weather'][0]['description']
            icon = json_response['weather'][0]['icon']
            temp = json_response['main']['temp']
            feels_like = json_response['main']['feels_like']
            temp_min = json_response['main']['temp_min']
            temp_max = json_response['main']['temp_max']
            pressure = json_response['main']['pressure']
            humidity = json_response['main']['humidity']
            sunrise = json_response['sys']['sunrise']
            sunset = json_response['sys']['sunset']
            timestamp = json_response['dt']
            dt_object = datetime.fromtimestamp(timestamp)
            current_date = dt_object.date()
            current_time = dt_object.time()

            current_weather_obj = CurrentWeatherResponse(city=city,
                 weather_desc=weather_desc,
                 icon=icon,
                 temp=temp,
                 feels_like=feels_like,
                 temp_min=temp_min,
                 temp_max=temp_max,
                 pressure=pressure,
                 humidity=humidity,
                 sunrise=sunrise,
                 sunset=sunset,
                 current_date=current_date,
                 current_time=current_time,
                 )

            return current_weather_obj
        else:
            code = response.status_code
            message = f'Произошла ошибка при выполнении запроса: {code}'
            error_obj = ErrorResponse(code=code, message=message)
            return error_obj

    def find_forecast_by_coords(self, lat, lon):
        """
        Метод находит прогноз погоды в городе по координатам (широта и долгота)
        :param lat: широта
        :param lon: долгота
        :return: объект класса ForecastWeatherResponse
        """
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()

            forecast_obj = ForecastWeatherResponse()

            name = json_response['city']['name']
            lat = json_response['city']['coord']['lat']
            lon = json_response['city']['coord']['lon']
            country = json_response['city']['country']
            city = CityResponse(name=name, lat=lat, lon=lon, country=country)
            sunrise = json_response['city']['sunrise']
            sunset = json_response['city']['sunset']

            for dt in json_response['list']:
                dt_object = datetime.fromtimestamp(dt['dt'])
                current_date = dt_object.date()
                current_time = dt_object.time()

                weather_desc = dt['weather'][0]['description']
                icon = dt['weather'][0]['icon']
                temp = dt['main']['temp']
                feels_like = dt['main']['feels_like']
                temp_min = dt['main']['temp_min']
                temp_max = dt['main']['temp_max']
                pressure = dt['main']['pressure']
                humidity = dt['main']['humidity']

                current_weather_obj = CurrentWeatherResponse(city=city,
                                                             weather_desc=weather_desc,
                                                             icon=icon,
                                                             temp=temp,
                                                             feels_like=feels_like,
                                                             temp_min=temp_min,
                                                             temp_max=temp_max,
                                                             pressure=pressure,
                                                             humidity=humidity,
                                                             sunrise=sunrise,
                                                             sunset=sunset,
                                                             current_date=current_date,
                                                             current_time=current_time,
                                                             )

                forecast_obj.forecast[dt['dt']] = current_weather_obj

            return forecast_obj

        else:
            code = response.status_code
            message = f'Произошла ошибка при выполнении запроса: {code}'
            error_obj = ErrorResponse(code=code, message=message)
            return error_obj

    def get_icon_from_openweathermap(self, icon):
        return f'https://openweathermap.org/img/wn/{icon}@2x.png'