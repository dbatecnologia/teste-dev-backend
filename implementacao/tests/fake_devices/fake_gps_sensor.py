#!/usr/bin/env python3

import unittest
import os
import time

import sys
sys.path.append('./fake_devices')

from fake_devices import fake_gps_sensor

fake_gps_port = '/dev/ttyACM100'
fake_gps = fake_gps_sensor.FakeGpsSensor(fake_gps_port)

def nmea_checksum(msg):
    start = msg.find('$') + 1
    end = msg.find('*', start)
    msg = msg[start:end]
    checksum = 0
    for char in msg:
       checksum ^= ord(char)
    return checksum

def get_nmea_checksum_from_msg(msg):
    start = msg.find('*') + 1
    msg = msg[start:len(msg)]
    return int(msg, 16)

class TestFakeGpsSensor(unittest.TestCase):
    def test_0_thread_is_alive(self):
        time.sleep(0.1)
        self.assertTrue(fake_gps.is_alive(), 'thread is not alive')

    def test_1_read_checksum(self):
        f_gps = open(fake_gps_port, 'r')
        msg = None
        for _ in range(0, 20):
            line = f_gps.readline()
            if 'GPRMC' in line:
                msg = line
                break
        f_gps.close()

        self.assertIsNotNone(msg, 'GPRMC string not found')
        checksum1 = nmea_checksum(msg)
        checksum2 = get_nmea_checksum_from_msg(msg)
        self.assertEqual(checksum1, checksum2, 'checksum is different')

    def test_2_stop(self):
        fake_gps.stop()
        fake_gps.join()
        self.assertFalse(fake_gps.is_alive(), 'thread is alive')

if __name__ == '__main__':
    unittest.main()
