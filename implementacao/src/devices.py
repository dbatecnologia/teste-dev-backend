#!/usr/bin/env python3

import gps
import gprs
import i2c_sensors

devices = None

def init(config):
    global devices
    if devices != None:
        return False
    if type(config) != dict:
        return False
    devices = Devices(
            config['i2c_sensors']['bus'],
            [
                config['i2c_sensors']['light_sensor_addr'],
                config['i2c_sensors']['distance_sensor_addr'],
                config['i2c_sensors']['battery_sensor_addr']
            ],
            config['gps']['port'],
            config['gps']['rate'],
            config['gprs']['port'],
            config['gprs']['rate'],
            config['gprs']['apn'])
    return True


class Devices:
    def __init__(self, i2c_bus=100, i2c_sensors_addr=[0x10,0x26,0x61],
            gps_port='/dev/ttyACM100', gps_rate=9600,
            gprs_port='/dev/ttyACM200', gprs_rate=9600,
            gprs_apn='tim.com.br'):

        self.light_sensor = i2c_sensors.LightSensor(i2c_sensors_addr[0],
                i2c_bus)
        self.distance_sensor = i2c_sensors.DistanceSensor(i2c_sensors_addr[1],
                i2c_bus)
        self.battery_sensor = i2c_sensors.BatterySensor(i2c_sensors_addr[2],
                i2c_bus)
        self.gps_sensor = gps.Gps(gps_port, gps_rate)
        self.modem = gprs.Gprs(gprs_port, gprs_rate)
        self.modem.open_connection(gprs_apn)

    def read(self):
        lat, lat_dir, lon, lon_dir = self.gps_sensor.get_position()
        data = {
                'light': self.light_sensor.read(),
                'distance': self.distance_sensor.read(),
                'battery': self.battery_sensor.read(),
                'gprs_connection': self.modem.is_connected(),
                'gps': {
                    'latitude': lat,
                    'latitude_direction': lat_dir,
                    'longitude': lon,
                    'longitude_direction': lon_dir
                }
            }
        return data
