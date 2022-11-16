import os.path
import xml.dom.minidom

from flaskr.data_model import CoordinatesDTO, DeviceDTO
import xml.etree.cElementTree as ET

from flaskr.datahandling.constants import DEVICES, SIMULATION_PARAMS, DEVICE, PATHS, COORDINATES, ID
from flaskr.datahandling.xml_utils import generate_file


class DeviceHandler:
    tree = None

    def __init__(self, filename: str):
        self.current_id = 1
        self.filename = filename
        if not os.path.isfile(filename):
            generate_file(filename)

    def get_tree(self):
        self.tree = ET.parse(self.filename)
        config = self.tree.getroot()
        devices = config.find(DEVICES)
        simulation_params = config.find(SIMULATION_PARAMS)
        return devices, simulation_params

    def save_xml(self):
        self.tree.write(self.filename)

    def add_device(self, deviceDTO: DeviceDTO) -> int:
        devices, simulation_params = self.get_tree()
        device = ET.SubElement(devices, DEVICE, id=str(self.current_id), name=deviceDTO.name)
        self.current_id = self.current_id + 1
        paths = ET.SubElement(device, PATHS)
        for coordinates in deviceDTO.path:
            ET.SubElement(paths, COORDINATES, latitude=str(coordinates.latitude), longitude=str(coordinates.longitude),
                          height=str(coordinates.height))
        self.save_xml()
        return self.current_id - 1

    def set_device_path(self, device_id: int, coordinatesDTOs):
        devices, simulation_params = self.get_tree()
        for device in devices:
            if device.attrib[ID] == device_id:
                paths = ET.SubElement(device, PATHS)
                for coordinates in coordinatesDTOs:
                    ET.SubElement(paths, "path", latitude=str(coordinates.latitude),
                                  longitude=str(coordinates.longitude),
                                  height=str(coordinates.height))
        return True

    def get_devices(self) -> []:
        devices_dtos = []
        devices, simulation_params = self.get_tree()
        for device in devices.iterfind(DEVICE):
            paths = []
            for p in device:
                for coordinates in p:
                    paths.append(CoordinatesDTO(coordinates.attrib['latitude'], coordinates.attrib['longitude'],
                                                coordinates.attrib['height']))
            devices_dtos.append(DeviceDTO(device.attrib['id'], device.attrib['name'], paths))
        return devices_dtos

    def get_device_path(self, device_id: str):
        device_path = []
        devices, simulation_params = self.get_tree()
        for device in devices:
            if device.attrib[ID] == device_id:
                for p in device:
                    for coordinates in p:
                        device_path.append(
                            CoordinatesDTO(coordinates.attrib['latitude'], coordinates.attrib['longitude'],
                                           coordinates.attrib['height']))
                    break;
        return device_path
