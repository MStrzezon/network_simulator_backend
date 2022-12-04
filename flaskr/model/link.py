from marshmallow import Schema, fields

from flaskr.model.device import Device


class Link(object):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class LinkSchema(Schema):
    source = fields.Str()
    destination = fields.Str()
