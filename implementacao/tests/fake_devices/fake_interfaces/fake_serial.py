#!/usr/bin/env python3

import unittest

from fake_devices.fake_interfaces import fake_serial

fake_serial_name = '/tmp/ttyACM0_unittest';
fake_ser = fake_serial.FakeSerial(fake_serial_name);

class TestFakeSerial(unittest.TestCase):
    def test_0_open(self):
        """
        Test that it can sum a list of integers
        """
        fake_ser.open()
        self.assertEqual(6, 6)

    def test_1_write(self):
        msg = 'test write!!!'
        ret = fake_ser.write(msg)
        self.assertEqual(len(msg), ret)

    def test_2_close(self):
        fake_ser.close()
        self.assertEqual(6, 6)

if __name__ == '__main__':
    unittest.main()
