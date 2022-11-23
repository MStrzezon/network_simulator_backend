from pysondb import db

devices_db = db.getDb('flaskr/datahandling/resources/devices.json')
simulation_db = db.getDb('flaskr/datahandling/resources/simulation_params.json')


def collect_data():
    devices = devices_db.getAll()
    simulation_params = simulation_db.getAll()
    if len(devices) < 2:
        return None, 'Simulation need to have minimum 2 devices'
    if not simulation_params:
        return None, 'Simulation need to have defined simulation params'
    return get_simulation_data(devices, simulation_params), 'OK'


def get_simulation_data(devices, simulation_params):
    simulation_data = dict()
    simulation_data['devices'] = devices
    simulation_data['simulation_params'] = simulation_params[0]
    return simulation_data
