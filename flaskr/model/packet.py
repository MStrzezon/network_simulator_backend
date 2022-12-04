from marshmallow import Schema, fields


class Packet(object):
    def __init__(self, source, destination, rssi, snr, duration, calculated_ber, payload, packet_type, lost):
        self.source = source
        self.destination = destination
        self.rssi = rssi
        self.snr = snr
        self.duration = duration
        self.calculated_ber = calculated_ber
        self.payload = payload
        self.packet_type = packet_type
        self.lost = lost

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class PacketSchema(Schema):
    tx = fields.Str()
    rx = fields.Str()
    source = fields.Str()
    destination = fields.Str()
    hops = fields.List(fields.Str())
    rssi = fields.Number()
    snr = fields.Number()
    duration = fields.Number()
    payload = fields.Str()
    lost = fields.Boolean()
