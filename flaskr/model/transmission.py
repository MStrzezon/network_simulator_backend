from marshmallow import Schema, fields


class Transmission(object):
    def __init__(self, data, interval, length, destination):
        self.data = data
        self.interval = interval
        self.length = length
        self.destination = destination

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class TransmissionSchema(Schema):
    data = fields.Str()
    interval = fields.Number()
    length = fields.Number()
    destination = fields.Str()
