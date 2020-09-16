#!/usr/bin/env python3

import unittest
import os
import time
import signal
import termios

import sys
sys.path.append('./fake_devices')

from fake_devices import fake_gprs

fake_gprs_port = '/dev/ttyACM200'
fake_gprs_dev = fake_gprs.FakeGprs(fake_gprs_port)

def timeout(sig, frm):
    raise Exception('read timeout')


def set_termios(fd):
    try:
        old_settings = termios.tcgetattr(fd)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = old_settings
    except termios.error as e:
        raise Exception('termios error: ' + repr(e))

    # set up raw mode / no echo / binary
    cflag |= (termios.CLOCAL | termios.CREAD)
    lflag &= ~(termios.ICANON | termios.ECHO | termios.ECHOE |
               termios.ECHOK | termios.ECHONL |
               termios.ISIG | termios.IEXTEN)  # |termios.ECHOPRT
    for flag in ('ECHOCTL', 'ECHOKE'):  # netbsd workaround for Erk
        if hasattr(termios, flag):
            lflag &= ~getattr(termios, flag)

    oflag &= ~(termios.OPOST | termios.ONLCR | termios.OCRNL)
    iflag &= ~(termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IGNBRK)
    if hasattr(termios, 'IUCLC'):
        iflag &= ~termios.IUCLC
    if hasattr(termios, 'PARMRK'):
        iflag &= ~termios.PARMRK

    termios.tcsetattr(fd, termios.TCSANOW,
            [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])


def read_cfg(at, timeout_s=5):
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(timeout_s)

    fd = os.open(fake_gprs_port, os.O_RDWR|os.O_NOCTTY)
    set_termios(fd)
    f_gprs = open(fd, 'wb+', buffering=0)
    w_size = f_gprs.write(at.encode())
    time.sleep(0.3)
    lines = list()
    while True:
        try:
            data = f_gprs.readline().decode()
        except:
            break
        lines.append(data)
        if 'OK' in data or 'ERROR' in data:
            break
    f_gprs.close()
    lines = ''.join(lines)
    # disable alarm
    signal.alarm(0)
    return w_size, lines


class TestFakeGprs(unittest.TestCase):
    def test_0_thread_is_alive(self):
        time.sleep(0.1)
        self.assertTrue(fake_gprs_dev.is_alive(), 'thread is not alive')

    def test_1_ate1(self):
        at = 'ATE1\r\n'
        w_size , lines = read_cfg(at)
        self.assertEqual(w_size, len(at),
                'write size and lenght of the at is not the same')
        self.assertIn('OK', lines, 'OK string not found')

    def test_2_atcops(self):
        at = 'AT+COPS?\r\n'
        w_size , lines = read_cfg(at)
        self.assertEqual(w_size, len(at),
                'write size and lenght of the at is not the same')
        self.assertIn('+COPS', lines, '+COPS string not found')

    def test_3_atcgdcont(self):
        at = 'AT+CGDCONT?\r\n'
        w_size , lines = read_cfg(at)
        self.assertEqual(w_size, len(at),
                'write size and lenght of the at is not the same')
        self.assertIn('+CGDCONT', lines, '+CGDCONT string not found')

    def test_4_error(self):
        at = 'test_wrong_at\r\n'
        w_size , lines = read_cfg(at)
        self.assertEqual(w_size, len(at),
                'write size and lenght of the at is not the same')
        self.assertIn('ERROR', lines, 'ERROR string not found')

    def test_5_stop(self):
        fake_gprs_dev.stop()
        fake_gprs_dev.join()
        self.assertFalse(fake_gprs_dev.is_alive(), 'thread is alive')

if __name__ == '__main__':
    unittest.main()
