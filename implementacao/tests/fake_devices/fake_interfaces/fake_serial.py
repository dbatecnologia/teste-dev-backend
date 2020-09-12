#!/usr/bin/env python3

import unittest
import os

from fake_devices.fake_interfaces import fake_serial

fake_serial_name = '/tmp/ttyACM0_unittest';
fake_ser = fake_serial.FakeSerial(None);

class TestFakeSerial(unittest.TestCase):
    def test_0_open(self):
        fake_ser.port = fake_serial_name
        fake_ser.open()
        path_exists = os.path.exists(os.readlink(fake_ser.port))
        self.assertTrue(path_exists, 'open failed')

    def test_1_write(self):
        msg = 'test write!!!'
        ret = fake_ser.write(msg)
        self.assertEqual(len(msg), ret, 'write failed')

    def test_2_close(self):
        pty = fake_ser.pty()
        fake_ser.close()
        path_exists = os.path.exists(fake_ser.port)
        self.assertFalse(path_exists, 'close failed: symlink')
        path_exists = os.path.exists(pty)
        self.assertFalse(path_exists, 'close failed: pty')

if __name__ == '__main__':
    unittest.main()
