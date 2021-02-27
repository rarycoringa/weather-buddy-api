import os, requests

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
        weather = {
            'city': response['name'],
            'temp': response['main']['temp'],
            'weather': response['weather'][0]['description'].title()
        }
    except:
        return {'message': 'Weather not found'}, 404

    return weather
