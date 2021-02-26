from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
        return {'greeting': 'Hello, DevGrid!'}

class WeatherCityList(Resource):
    def get(self):

        cities = [{'name': 'Floripa'}, {'name': 'Natal'}]
        return {'cities': cities}

class WeatherCity(Resource):
    def get(self, city_name):
        return {'city': city_name}

api.add_resource(Index, '/')
api.add_resource(WeatherCityList, '/weather')
api.add_resource(WeatherCity, '/weather/<string:city_name>')
