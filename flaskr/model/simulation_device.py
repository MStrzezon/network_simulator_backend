from marshmallow import Schema, fields


class SimulationDevice(object):
    def __init__(self, name, lat, lon, alt):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class SimulationDeviceSchema(Schema):
    name = fields.Str()
    lat = fields.Number()
    lon = fields.Number()
    alt = fields.Number()
