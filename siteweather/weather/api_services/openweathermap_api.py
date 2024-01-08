import requests
from ENV import API_KEY
from dto_response.city_response import CityResponse
from dto_response.error_response import ErrorResponse



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
                    state = res['state'] if 'state' in res else None
                    city_obj = CityResponse(name=name, lat=lat, lon=lon, country=country, state=state)
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



# city = input()
city = 'London'
limit = 2
url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={API_KEY}'
response = requests.get(url)

if response.status_code == 200:
    print('Запрос выполнен успешно')
    json_response = response.json()
    print('Ответ сервера в формате JSON:')
    print(len(json_response))
    for city in json_response:
        print(city)

        lat = city['lat']
        lon = city['lon']
        url_city_koords = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
        response_city = requests.get(url_city_koords)
        if response_city.status_code == 200:
            print('Запрос на погоду в городе выполнен успешно')
            json_response_city = response_city.json()
            print(json_response_city)
        else:
            print('Произошла ошибка при выполнении запроса:', response_city.status_code)

else:
    print('Произошла ошибка при выполнении запроса:', response.status_code)
