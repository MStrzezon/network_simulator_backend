import json
import os

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
