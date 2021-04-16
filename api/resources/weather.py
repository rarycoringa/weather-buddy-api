from flask import request
from flask_restful import Resource, reqparse
from api import cache
from api.requests.weather import request_openweathermap
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
    @cache.cached()
    def get(self, city_name):

        # Request the weather in the specify city
        weather = request_openweathermap(city_name)

        # Recover and update the weather list in the cache
        if isinstance(weather, Weather):
            weather_list = cache.get('weather_list') if cache.get('weather_list') is not None else []
            weather_list.append(weather.to_primitive())
            cache.set('weather_list', weather_list)
        else:
            return weather

        return weather.to_primitive(), 200
