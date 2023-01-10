from marshmallow import Schema, fields, post_dump, post_load

from flaskr.model.device import Device, DeviceSchema
from flaskr.model.link import LinkSchema
from flaskr.model.packet import Packet, PacketSchema
from flaskr.model.simulation_device import SimulationDevice, SimulationDeviceSchema


class Frame(object):
    def __init__(self, time, devices, packets):
        self.time = time
        self.devices = devices
        self.packets = packets


class FrameSchema(Schema):
    time = fields.Integer()
    devices = fields.Nested(SimulationDeviceSchema, many=True)
    packets = fields.Nested(PacketSchema, many=True, default=[])

    @post_load
    def change_none_to_empty_list(self, data, **kwargs):
        if not ('packets' in data.keys()):
            data['packets'] = []
        return data
