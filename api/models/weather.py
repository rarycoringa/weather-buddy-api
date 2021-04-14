from schematics.models import Model
from schematics.types import FloatType, GeoPointType, ModelType, StringType

class PhysicalQuantity(Model):
    value = FloatType(required=True)
    unit = StringType(required=True)


class City(Model):
    name = StringType(required=True)
    country = StringType()
    coordinates = GeoPointType()

    class Options:
        serialize_when_none = False


class Wind(Model):
    speed = ModelType(PhysicalQuantity, required=True)
    degree = ModelType(PhysicalQuantity, required=True)

    class Options:
        serialize_when_none = False


class Weather(Model):
    city = ModelType(City, required=True)
    description = StringType(required=True)
    long_description = StringType(required=True)
    temperature = ModelType(PhysicalQuantity, required=True)
    feels_like = ModelType(PhysicalQuantity)
    max_temperature = ModelType(PhysicalQuantity)
    min_temperature = ModelType(PhysicalQuantity)
    wind = ModelType(Wind, required=True)
    visibility = ModelType(PhysicalQuantity)

    class Options:
        serialize_when_none = False
