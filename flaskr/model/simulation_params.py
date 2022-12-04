from marshmallow import Schema, fields


class SimulationParams(object):
    def __init__(self, spreading_factor, bandwidth, phy_header_length):
        self.spreading_factor = spreading_factor
        self.bandwidth = bandwidth
        self.phy_header_length = phy_header_length

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)

    # @staticmethod
    # def from_json(self, json):
    #     self.param1 = json['param1']
    #     self.param2 = json['param2']
    #     self.param3 = json['param3']


class SimulationParamsSchema(Schema):
    spreading_factor = fields.Integer(required=True)
    bandwidth = fields.Number(required=True)
    phy_header_length = fields.Integer(required=True)
