from marshmallow import Schema, fields

from flaskr.model.coordinates import CoordinatesSchema
from flaskr.model.radio_params import RadioParamsSchema


class Device(object):
    def __init__(self, name, radio_params, path):
        self.name = name
        self.radio_params = radio_params
        self.path = path
        self.type = type

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class DeviceSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    radio_params = fields.Nested(RadioParamsSchema)
    path = fields.Nested(CoordinatesSchema, many=True)
    type = fields.Str()
