#!/usr/bin/env python3

import time
import fake_i2c_sensor
import fake_gps_sensor
import fake_gprs
from fake_interfaces import fake_i2c

# 0 to 100
LIGHT_SENSOR_VALUE_LIST = list(range(0, 101))

# 0cm to 255cm
DISTANCE_SENSOR_VALUE_LIST = list(range(0, 256))

# 120dV to 90dV (12V to 9V  - values in decivolts)
BATTERY_SENSOR_VALUE_LIST = list(range(120, 90, -1))

def main():
    i2c_bus = fake_i2c.FakeI2cBus(100, [0x10, 0x26, 0x61])

    light_sensor = fake_i2c_sensor.FakeI2cSensor(i2c_bus, 0x10, 0x00,
            LIGHT_SENSOR_VALUE_LIST)

    distance_sensor = fake_i2c_sensor.FakeI2cSensor(i2c_bus, 0x26, 0x00,
            DISTANCE_SENSOR_VALUE_LIST)

    battery_sensor = fake_i2c_sensor.FakeI2cSensor(i2c_bus, 0x61, 0x00,
            BATTERY_SENSOR_VALUE_LIST)

    gps = fake_gps_sensor.FakeGpsSensor('/dev/ttyACM100')

    gprs = fake_gprs.FakeGprs('/dev/ttyACM200')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('stopping...')

        light_sensor.stop()
        distance_sensor.stop()
        battery_sensor.stop()
        gps.stop()
        gprs.stop()

        light_sensor.join()
        distance_sensor.join()
        battery_sensor.join()
        gps.join()
        gprs.join()

        i2c_bus.close()

if __name__ == "__main__":
    main()
