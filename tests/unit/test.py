from flaskr.data_model import *
from flaskr.datahandling.devices_handling import DeviceHandler

device1 = DeviceDTO('0', "test1", [CoordinatesDTO('1', '1', '1'), CoordinatesDTO('2', '2', '2')])
device2 = DeviceDTO('0', "test2", [CoordinatesDTO('1', '1', '2'), CoordinatesDTO('2', '1', '1')])
device3 = DeviceDTO('0', "test3", [CoordinatesDTO('2', '2', '2'), CoordinatesDTO('3', '3', '3')])

device_handler = DeviceHandler(filename='../../tests/unit/resources/config.xml')

device_handler.add_device(device1)
device_handler.add_device(device2)
device_handler.add_device(device3)

