"""
Здесь описан класс для хранения данных по ответу с найденным городом
"""


class CityResponse:
    """
    Класс для хранения данных по ответу с найденным городом
    """
    def __init__(self, name, lat, lon, country, state=None):
        """
        В инициализатор попадают данные из JSON ответа от сервера API
        :param name: название города
        :param lat: широта
        :param lon: долгота
        :param country: страна
        :param state: штат (если есть, по умолчанию None)
        """
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country
        self.state = state

    def __str__(self):
        return str(f"{self.__class__.__name__}({self.name}, {self.lat}, {self.lon}, {self.country}, {self.state})")