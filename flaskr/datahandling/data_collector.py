import json
from typing import List, Dict, Any

from pysondb import db

devices_db = db.getDb('flaskr/datahandling/resources/devices.json')
simulation_db = db.getDb('flaskr/datahandling/resources/simulation_params.json')


def collect_data():
    devices = devices_db.getAll()
    devices = processDevices(devices)
    simulation_params = simulation_db.getAll()[0]
    del simulation_params['id']
    if len(devices) < 2:
        return None, 'Simulation need to have minimum 2 devices'
    if not simulation_params:
        return None, 'Simulation need to have defined simulation params'
    get_simulation_data(devices, simulation_params), 'OK'


def processDevices(devices: List[Dict[str, Any]]):
    for device in devices:
        del device['id']
        if len(device['transmissions']) == 0:
            del device['transmissions']
    return devices

def get_simulation_data(devices, simulation_params):
    simulation_data = dict()
    simulation_data['settings'] = simulation_params
    simulation_data['devices'] = devices
    with open('flaskr/framesextraction/resources/simulation_params.json', "w") as file:
        file.write(json.dumps(simulation_data, indent=2))
