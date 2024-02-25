from marshmallow import Schema, fields


class TemperatureSchema(Schema):
    temperature = fields.Float(required=True)
