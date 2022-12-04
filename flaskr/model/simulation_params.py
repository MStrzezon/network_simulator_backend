from marshmallow import Schema, fields


class SimulationParams(object):
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.type = type

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)

    @staticmethod
    def from_json(self, json):
        self.param1 = json['param1']
        self.param2 = json['param2']
        self.param3 = json['param3']


class SimulationParamsSchema(Schema):
    id = fields.Str()
    param1 = fields.Str()
    param2 = fields.Str()
    param3 = fields.Str()
