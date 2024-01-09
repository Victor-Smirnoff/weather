from weather.api_services.ISO_country_codes import countries

"""
Здесь описан класс для хранения данных по ответу с найденным городом
"""


class CityResponse:
    """
    Класс для хранения данных по ответу с найденным городом
    """
    def __init__(self, name, lat, lon, country):
        """
        В инициализатор попадают данные из JSON ответа от сервера API
        :param name: название города
        :param lat: широта
        :param lon: долгота
        :param country: страна
        """
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country
        self.country_name = countries[self.country]

    def __str__(self):
        return str(f"{self.__class__.__name__}({self.name}, {self.lat}, {self.lon}, {self.country}, {self.country_name})")