from flask import Blueprint, request
from marshmallow import ValidationError
from pysondb import db

from flaskr.model.simulation_params import SimulationParamsSchema

simulation_db = db.getDb('flaskr/datahandling/resources/simulation_params.json')

simulation_params_blueprint = Blueprint('simulation/params', __name__)


@simulation_params_blueprint.route("", methods=['POST'])
def add_simulation_params():
    schema = SimulationParamsSchema()
    try:
        simulation_params = SimulationParamsSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages, 400
    simulation_db.deleteAll()
    simulation_db.add(simulation_params)
    return schema.dump(simulation_db.getAll()[0])


@simulation_params_blueprint.route("", methods=['GET'])
def get_simulation_params():
    schema = SimulationParamsSchema()
    simulation_params_list = simulation_db.getAll()
    if simulation_params_list:
        simulation_params = simulation_params_list[0]
    else:
        simulation_params = simulation_params_list
    return schema.dump(simulation_params)
