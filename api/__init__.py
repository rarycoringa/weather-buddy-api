from flask import Flask, Blueprint
from flask_restful import Api

from api.resources.index import IndexView
from api.resources.weather import WeatherCityListView, WeatherCityView

# Create a Flask App instance
app = Flask(__name__)

# Create a Flask RESTful Api instance
api = Api(app)

# Add Api endpoints
api.add_resource(IndexView, '/', endpoint='index')
api.add_resource(WeatherCityListView, '/weather', endpoint='weather_city_list')
api.add_resource(WeatherCityView, '/weather/<string:city_name>', endpoint='weather_city')
