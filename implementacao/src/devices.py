#!/usr/bin/env python3

import gps
import gprs
import i2c_sensors

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
