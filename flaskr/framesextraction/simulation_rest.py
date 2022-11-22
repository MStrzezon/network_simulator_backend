from flask import Blueprint


simulation_blueprint = Blueprint('simulation', __name__)


@simulation_blueprint.route("/status", methods=['GET'])
def check_simulation_status():
    return None


@simulation_blueprint.route("/available-frames", methods=['GET'])
def check_available_frames():
    return None


@simulation_blueprint.route("/is-chunk-ready", methods=['GET'])
def is_chunk_ready():
    return None


@simulation_blueprint.route("/extract-frame", methods=['GET'])
def extract_frame():
    return None
