import xml.etree.cElementTree as ET
from flaskr.datahandling.constants import DEVICES, SIMULATION_PARAMS


def generate_file(filename: str):
    config = ET.Element("config")
    ET.SubElement(config, DEVICES)
    ET.SubElement(config, SIMULATION_PARAMS)
    ET.ElementTree(config).write(filename)
