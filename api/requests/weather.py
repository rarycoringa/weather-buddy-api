import requests

def request_openweathermap(city_name):
    '''
    Performs the request in the OpenWeatherMap API
    using the city name (city_name) and validates
    the request and the data.
    '''

    BASE_URL = 'api.openweathermap.org/data/2.5/weather'
    API_KEY = '3f62164f8ce1f8cb5ae8e2d02918babb'

    payload = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric',
    }

    try:
        response = requests.get(f'https://{BASE_URL}', params=payload).json()
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
