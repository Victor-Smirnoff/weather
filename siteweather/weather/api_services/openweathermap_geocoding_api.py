import requests
from ENV import API_KEY

# city = input()
city = 'London'

url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}'
response = requests.get(url)

if response.status_code == 200:
    print('Запрос выполнен успешно')
    json_response = response.json()
    print('Ответ сервера в формате JSON:')
    print(len(json_response))
    for city in json_response:
        print(city)
else:
    print('Произошла ошибка при выполнении запроса:', response.status_code)
