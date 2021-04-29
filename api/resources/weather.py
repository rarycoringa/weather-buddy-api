from flask import request
from flask_restful import Resource, reqparse
from unidecode import unidecode
from api import cache
from api import openweathermap as owm
from api.models.weather import Weather

class WeatherListView(Resource):
    def get(self):
        # Get the maximum size list parameter of weather list
        max = request.args.get('max') if request.args.get('max') is not None else 5

        # Validate the 'max' parameter (returns 400 if not an integer or less than or equal to zero)
        try:
            max = int(max)

            if max <= 0 or max > 5:
                raise Exception
        except:
            return {'message': 'The \'max\' attribute must be a positive integer between 1 and 5. Example: 4'}, 400

        # Recover and manage the weather list in the cache
        weather_list = cache.get('weather_list') if cache.get('weather_list') is not None else []

        if len(weather_list) == 0:
            return {'message': 'Weather list not found'}, 404

        weather_list.reverse()
        recent_weather_list = weather_list[:max]

        return recent_weather_list, 200

class WeatherView(Resource):
    def get(self, city_name):

        # Recovers the cached weather list
        weather_list = cache.get('weather_list')

        weather_cached = None

        for weather in weather_list:
            # Gets the weather in cache if exists
            if unidecode(city_name.upper()) == weather['id']:
                weather_cached = weather

        if weather_cached is not None:
            # Instances an existing weather in cache
            response = Weather(weather_cached)
        else:
            # Requests a new weather with the OpenWeatherMap API
            response = owm.current_weather(city_name)
            weather_list.append(response.to_primitive())
            cache.set('weather_list', weather_list)

        # Creates the context of the units of measurement
        if isinstance(response, Weather):
            weather = response

            # Creates the temperature context
            temperature = request.args.get('temperature', 'kelvin')
            temperature_context = {'temperature': temperature}
            weather.temperature.context = temperature_context
            if weather.feels_like is not None:
                weather.feels_like.context = temperature_context
            if weather.max_temperature is not None:
                weather.max_temperature.context = temperature_context
            if weather.min_temperature is not None:
                weather.min_temperature.context = temperature_context

            # Creates the distance context
            distance = request.args.get('distance', 'meters')
            distance_context = {'distance': distance}
            weather.visibility.context = distance_context
        else:
            return response

        return weather.to_primitive(), 200
