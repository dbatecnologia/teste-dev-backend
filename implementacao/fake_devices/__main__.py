#!/usr/bin/env python3

import time
import fake_i2c_sensor
import fake_interfaces.fake_i2c

# 0 to 100
LIGHT_SENSOR_VALUE_LIST = list(range(0, 101))

# 0cm to 255cm
DISTANCE_SENSOR_VALUE_LIST = list(range(0, 256))

# 90dV to 120dV (9V to 12V  - values in decivolts)
BATTERY_SENSOR_VALUE_LIST = list(range(90, 121))

def main():
    bus = fake_interfaces.fake_i2c.FakeI2cBus(100, [0x10, 0x26, 0x61])

    light_sensor = fake_i2c_sensor.FakeI2cSensor(bus, 0x10, 0x00,
            LIGHT_SENSOR_VALUE_LIST)

    distance_sensor = fake_i2c_sensor.FakeI2cSensor(bus, 0x26, 0x00,
            DISTANCE_SENSOR_VALUE_LIST)

    battery_sensor = fake_i2c_sensor.FakeI2cSensor(bus, 0x61, 0x00,
            BATTERY_SENSOR_VALUE_LIST)

    light_sensor.start()
    distance_sensor.start()
    battery_sensor.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
