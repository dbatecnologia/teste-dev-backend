import time

import gps
import gprs
import i2c_sensors

class Devices:
    def __init__(self):
        self.init_devices()

    def init_devices(self):
        self.light_sensor     = i2c_sensors.LightSensor(0x10)
        self.distance_sensor  = i2c_sensors.DistanceSensor(0x26)
        self.battery_sensor   = i2c_sensors.BatterySensor(0x61)
        self.gps_sensor       = gps.Gps()
        self.modem            = gprs.Gprs()

        self.modem.open_connection('tim.com.br')

    def run(self):
        while True:
            print('----')
            print(self.light_sensor.read())
            print(self.distance_sensor.read())
            print(self.battery_sensor.read())
            print(self.modem.is_connected())
            print(self.gps_sensor.get_position())
            time.sleep(0.5)
