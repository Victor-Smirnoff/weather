from weather.api_services.ISO_country_codes import countries

"""
Здесь описан класс для хранения данных по ответу с найденным городом
"""


class CityResponse:
    """
    Класс для хранения данных по ответу с найденным городом
    """
    def __init__(self, name, latitude, longitude, country):
        """
        В инициализатор попадают данные из JSON ответа от сервера API
        :param name: название города
        :param latitude: широта
        :param longitude: долгота
        :param country: страна
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.country = country
        self.country_name = countries[self.country]

    def __str__(self):
        return str(f"{self.__class__.__name__}({self.name}, {self.latitude}, {self.longitude}, {self.country}, {self.country_name})")