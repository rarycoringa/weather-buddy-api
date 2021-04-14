from schematics.models import Model
from schematics.types import BaseType, FloatType, GeoPointType, ModelType, StringType

class City(Model):
    name = StringType(required=True)
    country = StringType()
    coordinates = GeoPointType()

    class Options:
        serialize_when_none = False

class Wind(Model):
    speed = FloatType(required=True)
    degree = FloatType(required=True)

    class Options:
        serialize_when_none = False

class Weather(Model):
    city = ModelType(City, required=True)
    description = StringType(required=True)
    long_description = StringType(required=True)
    temperature = FloatType(required=True)
    feels_like = FloatType()
    max_temperature = FloatType()
    min_temperature = FloatType()
    wind = ModelType(Wind, required=True)
    visibility = FloatType()

    class Options:
        serialize_when_none = False
