from flask import Blueprint, jsonify
from pysondb import db

from flaskr.datahandling.data_collector import collect_data
from threading import Thread

from flaskr.framesextraction.simulation import simulate, FramesService

frames_db = db.getDb('flaskr/framesextraction/resources/frames.json')

simulation_blueprint = Blueprint('simulation', __name__)

framesService = FramesService()

@simulation_blueprint.route("", methods=['PUT'])
def start_simulation():
    collect_data()
    thread = Thread(target=simulate, args=(10,))
    thread.start()
    return jsonify('OK')


@simulation_blueprint.route("/reset", methods=['PUT'])
def reset_simulation():
    frames_db.deleteAll()
    return jsonify('OK')


@simulation_blueprint.route("/status", methods=['GET'])
def check_simulation_status():
    return None


@simulation_blueprint.route("/available-frames", methods=['GET'])
def check_available_frames():
    return jsonify(len(frames_db.getAll()))


@simulation_blueprint.route("/is-chunk-ready", methods=['GET'])
def is_chunk_ready():
    return jsonify(len(frames_db.getAll()) != 0)


@simulation_blueprint.route("/extract-frame", methods=['GET'])
def extract_frame():
    # frame = frames_db.get()[0]
    # frames_db.deleteById(frame['id'])
    # del frame['id']
    return framesService.get_chunk()
