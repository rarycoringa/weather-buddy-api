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
        CELSIUS = 1
        FAHRENHEIT = 2
        KELVIN = 3

    @serializable(type=FloatType, serialized_name='value')
    def get_temperature(self, *args, **kwargs):
        if hasattr(self, 'context'):
            temperature = self.context.get('temperature', 'kelvin')

            if temperature.upper() == self.TemperatureMetrics.CELSIUS.name:
                value = round(self.value - 273.0, 2) # Converts Kelvin temperature to Celsius
            elif temperature.upper() == self.TemperatureMetrics.FAHRENHEIT.name:
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

            if unit.upper() == self.TemperatureMetrics.CELSIUS.name:
                unit = self.TemperatureMetrics.CELSIUS
            elif unit.upper() == self.TemperatureMetrics.FAHRENHEIT.name:
                unit = self.TemperatureMetrics.FAHRENHEIT
            else:
                unit = self.TemperatureMetrics.KELVIN
        else:
            unit = self.TemperatureMetrics.KELVIN
        return unit.name.lower()


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
    visibility = ModelType(PhysicalQuantity)

    class Options:
        serialize_when_none = False
