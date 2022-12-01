from marshmallow import Schema, fields

from flaskr.model.device import Device, DeviceSchema
from flaskr.model.link import LinkSchema
from flaskr.model.packet import Packet, PacketSchema
from flaskr.model.simulation_device import SimulationDevice, SimulationDeviceSchema


class Frame(object):
    def __init__(self, devices, packets, links):
        self.devices = devices
        self.packets = packets
        self.links = links

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class FrameSchema(Schema):
    devices = fields.Nested(SimulationDeviceSchema, many=True)
    packets = fields.Nested(PacketSchema, many=True)
    links = fields.Nested(LinkSchema, many=True)
