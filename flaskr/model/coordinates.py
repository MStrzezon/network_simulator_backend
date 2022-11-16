from marshmallow import Schema, fields


class Coordinates(object):
    def __init__(self, latitude, longitude, height):
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.type = type

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class CoordinatesSchema(Schema):
    latitude = fields.Number()
    longitude = fields.Number()
    height = fields.Number()
    type = fields.Str()
