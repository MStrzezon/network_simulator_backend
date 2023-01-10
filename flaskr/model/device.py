from marshmallow import Schema, fields

from flaskr.model.coordinates import CoordinatesSchema
from flaskr.model.transmission import TransmissionSchema


class Device(object):
    def __init__(self, name, tx_power, path, transmissions):
        self.name = name
        self.tx_power = tx_power
        self.path = path
        self.transmissions = transmissions

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class DeviceSchema(Schema):
    name = fields.Str()
    tx_power = fields.Number()
    path = fields.Nested(CoordinatesSchema, many=True)
    transmissions = fields.Nested(TransmissionSchema, many=True, allow_none=True)
