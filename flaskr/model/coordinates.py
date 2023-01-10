from marshmallow import Schema, fields


class Coordinates(object):
    def __init__(self, time, latitude, longitude, altitude):
        self.time = time
        self.lat = latitude
        self.lon = longitude
        self.alt = altitude
        self.type = type

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class CoordinatesSchema(Schema):
    time = fields.Number()
    lat = fields.Number()
    lon = fields.Number()
    alt = fields.Number()
    type = fields.Str()
