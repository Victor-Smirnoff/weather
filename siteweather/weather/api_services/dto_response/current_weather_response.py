"""
Здесь описан класс для хранения данных по ответу с текущей погодой в городе
"""


class CurrentWeatherResponse:
    """
    Класс для хранения данных по ответу с текущей погодой в городе
    """
    def __init__(self,
                 name,
                 lat,
                 lon,
                 country,
                 weather_desc,
                 icon,
                 temp,
                 feels_like,
                 temp_min,
                 temp_max,
                 pressure,
                 humidity,
                 sunrise,
                 sunset,
                 current_date,
                 current_time,
                 ):
        """
        В инициализатор попадают данные из JSON ответа от сервера API
        :param name: название города
        :param lat: широта
        :param lon: долгота
        :param country: страна
        :param weather_desc: описание погоды
        :param icon: текстовое представление иконки погоды
        :param temp: текущая температура
        :param feels_like: как ощущается текущая температура
        :param temp_min: минимальная температура
        :param temp_max: максимальная температура
        :param pressure: давление
        :param humidity: влажность
        :param sunrise: время восхода Солнца
        :param sunset: время заката Солнца
        :param current_date: текущая дата
        :param current_time: текущее время
        """
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country
        self.weather_desc = weather_desc
        self.icon = icon
        self.temp = temp
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.sunrise = sunrise
        self.sunset = sunset
        self.current_date = current_date
        self.current_time = current_time