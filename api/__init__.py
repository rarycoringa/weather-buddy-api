from flask import Flask
from flask_restful import Api
from flask_caching import Cache

from api.utils.openweathermap import OpenWeatherMap

import os

# Create and configure Flask App instance
app = Flask(__name__)

# Create and configure Flask Cache instance
cache = Cache(app,
    config={
        'CACHE_TYPE': 'flask_caching.backends.SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300
    }
)

cache.init_app(app)

# Create a Flask RESTful Api instance
api = Api(app)

# Create a OpenWeatherMap Api instance
openweathermap = OpenWeatherMap(
    settings = {
        'API_KEY': os.environ.get('OPENWEATHERMAP_TOKEN'),
        'BASE_URL': 'api.openweathermap.org',
        'VERSION': '2.5',
        'SERVICE': 'weather'
    }
)

# Import Api endpoints
from api.resources.index import IndexView
from api.resources.weather import WeatherListView, WeatherView

# Add Api endpoints
api.add_resource(IndexView, '/', endpoint='index')
api.add_resource(WeatherListView, '/weather', endpoint='weather_list')
api.add_resource(WeatherView, '/weather/<string:city_name>', endpoint='weather')
