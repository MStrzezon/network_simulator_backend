from marshmallow import Schema, fields

from flaskr.model.device import DeviceSchema
from flaskr.model.simulation_params import SimulationParams


class SimulationInputData(object):
    def __init__(self, settings, devices):
        self.settings = settings
        self.devices = devices

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class SimulationInputDataSchema(Schema):
    settings = fields.Nested(SimulationParams)
    devices = fields.Nested(DeviceSchema, many=True)
