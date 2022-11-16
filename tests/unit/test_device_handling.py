import os

from flaskr.data_model import CoordinatesDTO, DeviceDTO
from flaskr.datahandling.devices_handling import DeviceHandler
import filecmp
import unittest


class TestSum(unittest.TestCase):
    device1 = DeviceDTO('1', "test1", [CoordinatesDTO('1', '1', '1'), CoordinatesDTO('2', '2', '2')])
    device2 = DeviceDTO('2', "test2", [CoordinatesDTO('1', '1', '2'), CoordinatesDTO('2', '1', '1')])
    device3 = DeviceDTO('3', "test3", [CoordinatesDTO('2', '2', '2'), CoordinatesDTO('3', '3', '3')])

    def test_add_device(self):

        device_handler = DeviceHandler(filename='../../tests/unit/resources/config_test.xml')

        device_handler.add_device(self.device1)
        device_handler.add_device(self.device2)
        device_handler.add_device(self.device3)

        self.assertTrue(
            filecmp.cmp('../../tests/unit/resources/config_test.xml', '../../tests/unit/resources/config.xml'))

    def test_get_devices(self):
        device_handler = DeviceHandler(filename='../../tests/unit/resources/config.xml')
        devices_from_file = device_handler.get_devices()
        self.assertEquals([self.device1, self.device2, self.device3], devices_from_file)

    def test_get_device_path(self):
        device_handler = DeviceHandler(filename='../../tests/unit/resources/config.xml')
        device_path = device_handler.get_device_path(str(2))
        print(device_path)
        self.assertEquals(self.device2.path, device_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile('../../tests/unit/resources/config_test.xml'):
            os.remove('../../tests/unit/resources/config_test.xml')


if __name__ == '__main__':
    unittest.main()
