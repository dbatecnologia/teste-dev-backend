#!/usr/bin/env python3

import json

config = None

CONFIG_DEFAULT = {
        'tcp_port': 1234,
        'server': {
            'url': 'http://127.0.0.1:8080',
            'send_interval': 30
        },
        'i2c_sensors': {
            'bus': 100,
            'light_sensor_addr': 16,
            'distance_sensor_addr': 38,
            'battery_sensor_addr': 97
        },
        'gps': {
            'port': '/dev/ttyACM100',
            'rate': 9600
        },
        'gprs': {
            'port': '/dev/ttyACM200',
            'rate': 9600,
            'apn': 'tim.com.br'
        }
    }


def read_file(config_file):
    global config
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        if check_integrity(config):
            return True
        print('Checks config integrity fails. Using default config')
    except Exception as e:
        print('Read config file fails. Using default config: ' + repr(e))
    config = CONFIG_DEFAULT
    return False


def write_file(config_file):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)


def check_integrity(config):
    """
    Checks the integrity of the configuration file
    """
    if type(config['tcp_port']) is not int:
        return False

    # Server config
    if type(config['server']) is not dict:
        return False
    if type(config['server']['url']) is not str:
        return False
    if type(config['server']['send_interval']) is not int:
        return False

    # I2C sensors config
    if type(config['i2c_sensors']) is not dict:
        return False
    if type(config['i2c_sensors']['bus']) is not int:
        return False
    if type(config['i2c_sensors']['light_sensor_addr']) is not int:
        return False
    if type(config['i2c_sensors']['distance_sensor_addr']) is not int:
        return False
    if type(config['i2c_sensors']['battery_sensor_addr']) is not int:
        return False

    # GPS config
    if type(config['gps']) is not dict:
        return False
    if type(config['gps']['port']) is not str:
        return False
    if type(config['gps']['rate']) is not int:
        return False

    # GPRS config
    if type(config['gprs']) is not dict:
        return False
    if type(config['gprs']['port']) is not str:
        return False
    if type(config['gprs']['rate']) is not int:
        return False
    if type(config['gprs']['apn']) is not str:
        return False

    return True
