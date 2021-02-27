from flask import request
from flask_restful import Resource, reqparse

from api.requests.weather import request_openweathermap

class WeatherCityListView(Resource):
    def get(self):

        max = request.args.get('max') if request.args.get('max') is not None else 5

        try:
            max = int(max)

            if max <= 0:
                raise Exception
        except:
            return {'message': 'The \'max\' attribute must be a positive integer greater than zero. Example: 4.'}, 400

        cities = []

        for i in range(0, max):
            cities.append(request_openweathermap('London'))

        return cities

class WeatherCityView(Resource):
    def get(self, city_name):

        response = request_openweathermap(city_name)

        return response
