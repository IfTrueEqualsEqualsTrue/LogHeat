import serial.tools.list_ports as list_ports


def get_available_com_ports():
    """Returns a list of available COM ports on the computer."""
    ports = list_ports.comports()
    return [port.device for port in ports]
