"""
Здесь описан класс для хранения данных по ответу с прогнозом погоды в городе
"""


class ForecastWeatherResponse:
    """
    Класс для хранения данных по ответу с прогнозом погоды в городе
    Просто словарь forecast, в котором ключами будет время в формате UNIX типа 1704812400
    А значением будет объект класса CurrentWeatherResponse со всеми данными о погоде
    """
    forecast = {}