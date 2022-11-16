from marshmallow import Schema, fields


class SimulationParams(object):
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.type = type

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class SimulationParamsSchema(Schema):
    param1 = fields.Str()
    param2 = fields.Str()
    param3 = fields.Str()
