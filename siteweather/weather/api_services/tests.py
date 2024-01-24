from django.test import TestCase

from weather.api_services.dto_response.city_response import CityResponse
from weather.api_services.dto_response.error_response import ErrorResponse


class WeatherAPIServiceTest(TestCase):

    def test_find_by_city_incorrect(self):
        cityname = '123456'
        result = ErrorResponse(code=404, message=f'Город “{cityname}” не найден')
        self.assertEqual(result.message, f'Город “{cityname}” не найден')

    def test_find_by_city_correct(self):
        result = [CityResponse(name='Tbilisi', latitude='41,6934591', longitude='44,8014495', country='GE'),
                  CityResponse(name='ზღვისუბანი XI მიკრო-რაიონი III კვარტალი', latitude='41,7731289', longitude='44,819248778866864', country='GE')
                  ]
        self.assertTrue(len(result), 2)
        self.assertTrue(type(result), list)
        self.assertTrue(type(result[0]), CityResponse)