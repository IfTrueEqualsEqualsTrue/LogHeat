import serial.tools.list_ports as list_ports
from flask import jsonify


def get_available_com_ports():
    """Returns a list of available COM ports on the computer."""
    ports = list_ports.comports()
    return [port.device for port in ports]


def get_com_ports_json():
    """Returns the available COM ports as a JSON response."""
    ports = get_available_com_ports()
    return jsonify(ports=ports)
