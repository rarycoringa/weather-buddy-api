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
        json = requests.get(f'https://{BASE_URL}', params=payload).json()
    except:
        return {'message': 'Connection to the openweathermap service failed'}, 503

    try:
        response = {
            'city': json['name'],
            'temp': json['main']['temp'],
            'weather': json['weather'][0]['main']
        }
    except:
        return {'message': 'City not found'}, 404

    return response
