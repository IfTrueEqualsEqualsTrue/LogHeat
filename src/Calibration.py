""" File to manage the calibration of the conditionning circuit of the thermocouple. """
import os

import yaml

from PathConfig import base_path


def load_calibration():
    """ Load the calibration parameters for the thermocouple. """
    with open(os.path.join(base_path, 'ressources', 'calibration.yml'), 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def write_calibration(calibration):
    with open(os.path.join(base_path, 'ressources', 'calibration.yml'), 'w') as file:
        yaml.dump(calibration, file)


def get_calibration_parameters():
    """ Get the calibration parameters for the thermocouple. """
    calibration = load_calibration()
    return calibration['thermocouple']['coefficient'], calibration['thermocouple']['offset']


def apply_calibration(temperature):
    """ Apply the calibration to the temperature. """
    coefficient, offset = get_calibration_parameters()
    return temperature * coefficient + offset


def set_calibration_parameters(coefficient, offset):
    """ Set the calibration parameters for the thermocouple. """
    calibration = load_calibration()
    calibration['thermocouple']['coefficient'] = coefficient
    calibration['thermocouple']['offset'] = offset
    write_calibration(calibration)
