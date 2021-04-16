import os, requests
from api.models.weather import PhysicalQuantity, City, Wind, Weather

def request_openweathermap(city_name):
    '''
    Performs the request in the OpenWeatherMap API
    using the city name (city_name) and validates
    the request and the data.
    '''

    OPENWEATHERMAP_BASE_URL = 'api.openweathermap.org/data/2.5/weather'
    OPENWEATHERMAP_TOKEN = os.environ.get('OPENWEATHERMAP_TOKEN')

    payload = {
        'q': city_name,
        'appid': OPENWEATHERMAP_TOKEN,
        'units': 'metric',
    }

    try:
        response = requests.get(f'https://{OPENWEATHERMAP_BASE_URL}', params=payload).json()
    except:
        return {'message': 'Connection to the OpenWeatherMap API service failed'}, 503

    try:
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

        weather.validate()
    except:
        return {'message': 'Weather not found'}, 404

    return weather
