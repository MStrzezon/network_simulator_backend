from flask import request, Blueprint, jsonify
from flask_restx import Api
from marshmallow import ValidationError

from pysondb import db
from pysondb.errors import IdNotFoundError

from flaskr.datahandling.constants import PATH
from flaskr.model.coordinates import Coordinates, CoordinatesSchema
from flaskr.model.device import DeviceSchema

devices_db = db.getDb('flaskr/datahandling/resources/devices.json')

devices = Blueprint('devices', __name__, url_prefix="/devices")


@devices.route("/<int:device_id>", methods=['GET'])
def get_device_by_id(device_id):
    schema = DeviceSchema()
    try:
        device = devices_db.getById(device_id)
        return schema.dump(device)
    except IdNotFoundError as idNotFound:
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFound.pk))


@devices.route("", methods=['GET'])
def get_all_devices():
    schema = DeviceSchema(many=True)
    return schema.dump(devices_db.getAll())


@devices.route("", methods=['PUT'])
def add_device():
    schema = DeviceSchema()
    try:
        device = DeviceSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages
    device_id = devices_db.add(device)
    return schema.dump(devices_db.getById(device_id))


@devices.route("", methods=['DELETE'])
def remove_all_devices():
    devices_db.deleteAll()
    return jsonify(True)


@devices.route("/<int:device_id>", methods=['DELETE'])
def remove_device_by_id(device_id):
    devices_db.deleteById(device_id)
    return jsonify(True)


@devices.route("/device-path/<int:device_id>", methods=['GET'])
def get_device_path(device_id):
    schema = CoordinatesSchema(many=True)
    try:
        device = devices_db.getById(device_id)
        return schema.dump(device['path'])
    except IdNotFoundError as idNotFound:
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFound.pk))


@devices.route("/device-path/<int:device_id>", methods=['PUT'])
def add_device_path(device_id):
    try:
        path = CoordinatesSchema(many=True).load(request.get_json())
    except ValidationError as err:
        return err.messages
    try:
        device = devices_db.getById(device_id)
    except IdNotFoundError as idNotFound:
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFound.pk))
    device[PATH].extend(path)
    devices_db.updateById(pk=device_id, new_data=device)
    device_schema = DeviceSchema()
    return device_schema.dump(devices_db.getById(device_id))
