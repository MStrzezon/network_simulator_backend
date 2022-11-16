from flask import Blueprint, request
from marshmallow import ValidationError
from pysondb import db

from flaskr.model.simulation_params import SimulationParamsSchema

simulation_db = db.getDb('flaskr/datahandling/resources/simulation_params.json')

simulation = Blueprint('simulation', __name__)


@simulation.route("/params", methods=['PUT'])
def add_simulation_params():
    schema = SimulationParamsSchema()
    try:
        simulation_params = SimulationParamsSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages
    simulation_db.deleteAll()
    simulation_db.add(simulation_params)
    return schema.dump(simulation_db.getAll()[0])


@simulation.route("/params", methods=['GET'])
def get_simulation_params():
    schema = SimulationParamsSchema()
    simulation_params_list = simulation_db.getAll()
    if simulation_params_list:
        simulation_params = simulation_params_list[0]
    else:
        simulation_params = simulation_params_list
    return schema.dump(simulation_params)
