from flask import request, Blueprint, jsonify
from marshmallow import ValidationError

from pysondb import db
from pysondb.errors import IdNotFoundError

from flaskr.datahandling.constants import PATH
from flaskr.model.coordinates import CoordinatesSchema
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
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFound.pk)), 400


@devices.route("", methods=['GET'])
def get_all_devices():
    schema = DeviceSchema(many=True)
    return schema.dump(devices_db.getAll())


# TODO validate nested fields
@devices.route("", methods=['POST'])
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
    try:
        devices_db.deleteById(device_id)
    except IdNotFoundError as idNotFoundErr:
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFoundErr.pk)), 400
    return jsonify(True)


@devices.route("/<int:device_id>/device-path", methods=['GET'])
def get_device_path(device_id):
    schema = CoordinatesSchema(many=True)
    try:
        device = devices_db.getById(device_id)
        return schema.dump(device['path'])
    except IdNotFoundError as idNotFound:
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFound.pk)), 400


@devices.route("/<int:device_id>/device-path", methods=['PUT'])
def update_device_path(device_id):
    try:
        path = CoordinatesSchema(many=True).load(request.get_json())
    except ValidationError as err:
        return err.messages, 405
    try:
        device = devices_db.getById(device_id)
    except IdNotFoundError as idNotFound:
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFound.pk)), 400
    device[PATH].extend(path)
    devices_db.updateById(pk=device_id, new_data=device)
    device_schema = DeviceSchema()
    return device_schema.dump(devices_db.getById(device_id))


@devices.route("/<int:device_id>/device-path", methods=['DELETE'])
def clear_device_path(device_id):
    try:
        device = devices_db.getById(device_id)
    except IdNotFoundError as idNotFound:
        return jsonify('Device with id: {id} does not exists'.format(id=idNotFound.pk)), 400
    device[PATH].clear()
    devices_db.updateById(pk=device_id, new_data=device)
    device_schema = DeviceSchema()
    return device_schema.dump(devices_db.getById(device_id))
