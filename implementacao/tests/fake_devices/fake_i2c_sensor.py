#!/usr/bin/env python3

import unittest
import os
import time

from fake_devices.fake_interfaces import fake_i2c
from fake_devices import fake_i2c_sensor

fake_i2c_bus = 101
fake_i2c_devices = [0x28]
fake_i2c = fake_i2c.FakeI2cBus(fake_i2c_bus, fake_i2c_devices)
data = [0x56, 0xaa, 0xb0, 0xdf]

fake_sensor = fake_i2c_sensor.FakeI2cSensor(fake_i2c, fake_i2c_devices[0], 0x00,
        data)

def checksum(i2c_addr, value):
    """
    Calculates the checksum.
    """
    return (i2c_addr + value) & 0xff

class TestFakeI2cSensor(unittest.TestCase):
    def test_0_thread_is_alive(self):
        time.sleep(0.1)
        self.assertTrue(fake_sensor.is_alive(), 'thread is not alive')

    def test_1_read_checksum(self):
        read_data = fake_i2c.read_i2c_block_data(fake_i2c_devices[0], 0x00, 3)
        self.assertEqual(fake_i2c_devices[0], read_data[0],
                'i2c address is different')
        self.assertIn(read_data[1], data, 'data read is not in data list')
        check = checksum(fake_i2c_devices[0], read_data[1])
        self.assertEqual(check, read_data[2], 'checksum is different')

    def test_2_stop(self):
        fake_sensor.stop()
        fake_sensor.join()
        self.assertFalse(fake_sensor.is_alive(), 'thread is alive')

if __name__ == '__main__':
    unittest.main()
