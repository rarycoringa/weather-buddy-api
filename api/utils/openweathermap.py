import os, requests
from api.models.weather import PhysicalQuantity, City, Wind, Weather

class OpenWeatherMap:

    def __init__(self, settings):
        self.__api_key = settings['API_KEY']
        self._base_url = settings['BASE_URL']
        self._version = settings['VERSION']
        self._service = settings['SERVICE']

    @property
    def url(self):
        return f'https://{self._base_url}/data/{self._version}/{self._service}'

    @staticmethod
    def format_weather(response):
        weather = Weather({
            'city': City({
                'name': response['name'].title(),
                'country': response['sys']['country'].upper(),
                'coordinates': [response['coord']['lat'], response['coord']['lon']]
            }),
            'description': response['weather'][0]['main'].title(),
            'long_description': response['weather'][0]['description'].title(),
            'temperature': PhysicalQuantity({
                'value': float(response['main']['temp']),
                'unit': 'celsius degree'
            }),
            'feels_like': PhysicalQuantity({
                'value': float(response['main']['feels_like']),
                'unit': 'celsius degree'
            }) if response['main']['feels_like'] != response['main']['temp'] else None,
            'max_temperature': PhysicalQuantity({
                'value': float(response['main']['temp_max']),
                'unit': 'celsius degree'
            }) if response['main']['temp_max'] != response['main']['temp'] else None,
            'min_temperature': PhysicalQuantity({
                'value': float(response['main']['temp_min']),
                'unit': 'celsius degree'
            }) if response['main']['temp_min'] != response['main']['temp'] else None,
            'wind': Wind({
                'speed': PhysicalQuantity({
                    'value': float(response['wind']['speed']),
                    'unit': 'meters per second'
                }),
                'degree': PhysicalQuantity({
                    'value': float(response['wind']['deg']),
                    'unit': 'degrees'
                })
            }),
            'visibility': PhysicalQuantity({
                'value': float(response['visibility']),
                'unit': 'meters'
            })
        })

        return weather

    def current_weather(self, query):

        payload = {'q': query, 'appid': self.__api_key}

        try:
            response = requests.get(self.url, params=payload)

            if response.status_code != requests.codes.ok:
                response.raise_for_status()
        except:
            if response.status_code == requests.codes.not_found:
                return {'message': 'Weather not found'}, response.status_code
            else:
                return {'message': 'Connection to the OpenWeatherMap API service failed'}, response.status_code

        weather = self.format_weather(response.json())

        return weather


    def mock_request_city(self):

        response = {
            'coord': {'lon': -0.1257, 'lat': 51.5085},
            'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}],
            'base': 'stations',
            'main': {'temp': 281.86, 'feels_like': 280.06, 'temp_min': 280.93, 'temp_max': 282.59, 'pressure': 1019, 'humidity': 76},
            'visibility': 10000,
            'wind': {'speed': 3.09, 'deg': 90},
            'clouds': {'all': 91},
            'dt': 1618870982,
            'sys': {'type': 1, 'id': 1414, 'country': 'GB', 'sunrise': 1618808150, 'sunset': 1618858977},
            'timezone': 3600,
            'id': 2643743,
            'name': 'London',
            'cod': 200
        }

        return response, 200
