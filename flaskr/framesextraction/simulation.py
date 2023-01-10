import json
import os
from dataclasses import dataclass

from marshmallow import EXCLUDE
from pysondb import db

from flaskr.lorameshsimulator.main import basic_use
from flaskr.model.frame import FrameSchema

frames_db = db.getDb('flaskr/framesextraction/resources/frames.json')


def simulate(arg):
    basic_use('flaskr/framesextraction/resources/simulation_params.json', 'flaskr/framesextraction/resources'
                                                                          '/simulation_result')
    with open('flaskr/framesextraction/resources/simulation_result_1.json', "r") as simulation_result:
        frames = json.loads(simulation_result.read())
        for frame in frames:
            frame_schema = FrameSchema().load(frame)
            frames_db.add(frame_schema)
    os.remove('flaskr/framesextraction/resources/simulation_result_1.json')
    os.remove('flaskr/framesextraction/resources/simulation_params.json')


@dataclass(frozen=True)
class PacketTransmittedInfo:
    source: str
    destination: str

    def __eq__(self, other):
        return self.source == other.source and self.destination == other.destination


class FramesService:
    def reset(self):
        self.current_time = 0
        self.delay = 0
        self.throughput = 0
        self.packets_transmitted = []
        self.data_sent = 0
        self.data_received = 0
        self.data_forwarded = 0

    def __init__(self):
        self.current_time = 0
        self.delay = 0
        self.throughput = 0
        self.packets_transmitted = dict()
        self.packets_received = dict()
        self.data_sent = 0
        self.data_received = 0
        self.data_forwarded = 0

    def get_chunk(self):
        frames = frames_db.getAll()
        if len(frames) > 10:
            frames_in_time = frames[0:10]
        else:
            frames_in_time = frames
        for frame in frames_in_time:
            for packet in frame['packets']:
                if len(packet.keys()) <= 1:
                    continue
                if packet['tx'] == packet['source']:
                    self.packets_transmitted[PacketTransmittedInfo(packet['source'], packet['destination'])] = frame[
                        'time']
                    self.data_sent += 1
                if packet['rx'] == packet['destination'] and not packet['lost']:
                    self.delay += (frame['time'] + packet['duration']) - \
                                  self.packets_transmitted[
                                      PacketTransmittedInfo(packet['source'], packet['destination'])]
                    self.data_received += 1
                if packet['rx'] != packet['destination'] and not packet['lost']:
                    self.data_forwarded += 1
            frame['normalized_routing_load'] = round((self.data_sent + self.data_forwarded) / self.data_received if self.data_received > 0 else 0, 2)
            frame['delivery_ratio'] = round(self.data_received / self.data_sent, 2)
            frame['average_delay'] = (self.delay * 10 ** (-3)) / self.data_received if self.data_received > 0 else 0
            frames_db.deleteById(frame['id'])

        return frames_in_time
