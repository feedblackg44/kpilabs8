from marshmallow import Schema, fields
from .temperature_schema import TemperatureSchema
from .gps_schema import GpsSchema


class AggregatedTemperatureSchema(Schema):
    temperature = fields.Nested(TemperatureSchema)
    gps = fields.Nested(GpsSchema)
    timestamp = fields.DateTime('iso')
