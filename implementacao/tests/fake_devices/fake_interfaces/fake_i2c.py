#!/usr/bin/env python3

import unittest
import os

from fake_devices.fake_interfaces import fake_i2c

fake_i2c_bus = 101
fake_i2c_devices = [0x05, 0x16, 0x27]
fake_i2c = fake_i2c.FakeI2cBus()
data = [0x03, 0x04, 0x05]

class TestFakeI2cBus(unittest.TestCase):
    def test_0_open(self):
        fake_i2c.open(fake_i2c_bus, fake_i2c_devices)
        path_exists = os.path.exists(os.readlink(fake_i2c.bus_path()))
        self.assertTrue(path_exists, 'load i2c module failed')

    def test_1_write(self):
        fake_i2c.write_i2c_block_data(fake_i2c_devices[0], 0x00, data)

    def test_2_read(self):
        read_data = fake_i2c.read_i2c_block_data(fake_i2c_devices[0], 0x00,
                len(data))
        self.assertEqual(data, read_data, 'read failed')

    def test_3_close(self):
        bus_path = fake_i2c.real_bus_path()
        bus_path_link = fake_i2c.bus_path()
        fake_i2c.close()
        path_exists = os.path.exists(bus_path_link)
        self.assertFalse(path_exists, 'unload i2c module failed: symlink')
        path_exists = os.path.exists(bus_path)
        self.assertFalse(path_exists, 'unload i2c module failed: smbus stub')

if __name__ == '__main__':
    unittest.main()
