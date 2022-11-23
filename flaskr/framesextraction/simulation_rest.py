import socketio
from flask import Blueprint, jsonify
from pysondb import db

from flaskr.datahandling.data_collector import collect_data
from flaskr.model.frame import Frame

frames_db = db.getDb('flaskr/framesextraction/resources/frames.json')

simulation_blueprint = Blueprint('simulation', __name__)

sio = socketio.Client()
# sio.connect('http://localhost:5000')


@simulation_blueprint.route("", methods=['PUT'])
def start_simulation():
    data, info = collect_data()
    if data is None:
        return jsonify(info), 400
    sio.emit('message', jsonify(data))
    return jsonify(info)


@sio.on('my event')
def get_frames_from_engine(frames):
    for frame_from_engine in frames:
        frame = Frame().load(frame_from_engine)
        frames_db.add(frame)


@simulation_blueprint.route("/status", methods=['GET'])
def check_simulation_status():
    return None


@simulation_blueprint.route("/available-frames", methods=['GET'])
def check_available_frames():
    return jsonify(len(frames_db.getAll()))


@simulation_blueprint.route("/is-chunk-ready", methods=['GET'])
def is_chunk_ready():
    return None


@simulation_blueprint.route("/extract-frame", methods=['GET'])
def extract_frame():
    frame = frames_db.get()
    return frame
