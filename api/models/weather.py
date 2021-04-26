from schematics.models import Model
from schematics.types import FloatType, GeoPointType, ModelType, StringType
from schematics.types.serializable import serializable
from enum import Enum

class PhysicalQuantity(Model):
    value = FloatType(required=True)
    unit = StringType(required=True)


class Temperature(Model):
    value = FloatType(required=True)

    class TemperatureMetrics(Enum):
        CELSIUS = 'celsius'
        FAHRENHEIT = 'fahrenheit'
        KELVIN = 'kelvin'

    @serializable(type=FloatType, serialized_name='value')
    def get_temperature(self, *args, **kwargs):
        if hasattr(self, 'context'):
            temperature = self.context.get('temperature', 'kelvin')

            if temperature.lower() == self.TemperatureMetrics.CELSIUS.value:
                value = round(self.value - 273.0, 2) # Converts Kelvin temperature to Celsius
            elif temperature.lower() == self.TemperatureMetrics.FAHRENHEIT.value:
                value = round(1.8*(self.value-273.0)+32.0, 2) # Converts Kelvin temperature to Fahrenheit
            else:
                value = round(self.value, 2) # Returns Kelvin temperature
        else:
            value = round(self.value, 2) # Returns Kelvin temperature
        return value

    @serializable(type=StringType, serialized_name='unit')
    def get_unit(self, *args, **kwargs):
        if hasattr(self, 'context'):
            unit = self.context.get('temperature', 'kelvin')

            if unit.lower() == self.TemperatureMetrics.CELSIUS.value:
                unit = self.TemperatureMetrics.CELSIUS
            elif unit.lower() == self.TemperatureMetrics.FAHRENHEIT.value:
                unit = self.TemperatureMetrics.FAHRENHEIT
            else:
                unit = self.TemperatureMetrics.KELVIN
        else:
            unit = self.TemperatureMetrics.KELVIN
        return unit.value


class Distance(Model):
    value = FloatType(required=True)

    class DistanceMetrics(Enum):
        METERS = 'meters'
        KILOMETERS = 'kilometers'
        MILES = 'miles'

    @serializable(type=FloatType, serialized_name='value')
    def get_distance(self, *args, **kwargs):
        if hasattr(self, 'context'):
            distance = self.context.get('distance', 'meters')

            if distance.lower() == self.DistanceMetrics.KILOMETERS.value:
                value = round(self.value / 1000, 2) # Converts Meters distance to Kilometers
            elif distance.lower() == self.DistanceMetrics.MILES.value:
                value = round(self.value / 1609.344, 2) # Converts Meters distance to Miles
            else:
                value = round(self.value, 2) # Returns Meters distance
        else:
            value = round(self.value, 2) # Returns Meters distance
        return value

    @serializable(type=StringType, serialized_name='unit')
    def get_unit(self, *args, **kwargs):
        if hasattr(self, 'context'):
            unit = self.context.get('distance', 'meters')

            if unit.lower() == self.DistanceMetrics.KILOMETERS.value:
                unit = self.DistanceMetrics.KILOMETERS
            elif unit.lower() == self.DistanceMetrics.MILES.value:
                unit = self.DistanceMetrics.MILES
            else:
                unit = self.DistanceMetrics.METERS
        else:
            unit = self.DistanceMetrics.METERS
        return unit.value


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
    temperature = ModelType(Temperature, required=True)
    feels_like = ModelType(Temperature)
    max_temperature = ModelType(Temperature)
    min_temperature = ModelType(Temperature)
    wind = ModelType(Wind, required=True)
    visibility = ModelType(Distance)

    class Options:
        serialize_when_none = False
