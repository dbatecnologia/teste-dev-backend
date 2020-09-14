#!/usr/bin/env python3

import unittest
import os

from fake_devices.fake_interfaces import fake_i2c

fake_i2c_bus = 101
fake_i2c_devices = [0x05, 0x16, 0x27]
fake_i2c = fake_i2c.FakeI2c(fake_i2c_bus);

import time

class TestFakeI2cBus(unittest.TestCase):
    def test_0_load_modules(self):
        fake_i2c.add_fake_devices(fake_i2c_devices)
        path_exists = os.path.exists(os.readlink(fake_i2c.bus_path()))
        self.assertTrue(path_exists, 'load i2c module failed')

    def test_1_unload_modules(self):
        bus_path = fake_i2c.real_bus_path()
        bus_path_link = fake_i2c.bus_path()
        fake_i2c.del_fake_devices()
        path_exists = os.path.exists(bus_path_link)
        self.assertFalse(path_exists, 'unload i2c module failed: symlink')
        path_exists = os.path.exists(bus_path)
        self.assertFalse(path_exists, 'unload i2c module failed: smbus stub')

if __name__ == '__main__':
    unittest.main()
