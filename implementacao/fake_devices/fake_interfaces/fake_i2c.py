#!/usr/bin/env python3
#
# References:
#  Article "Using the I2C-Stub to Emulate a Device"
#   (https://eraretuya.github.io/2016/12/10/the-i2c-stub-in-action/)
#  smbus2 (https://github.com/kplindegaard/smbus2)


# $ modprobe i2c-dev
# $ modprobe i2c-stub chip_addr=0x03
# $ i2cdetect -l
# ...
# i2c-8 smbus   SMBus stub driver   SMBus adapter
# ...
# $ i2cdetect -y 8
# $ modprobe -r i2c-stub # Remove module

import os
import subprocess

#import smbus
#import smbus2 as smbus
import smbus2

class FakeI2c:
    """
    Fake I2C bus implementation.
    """
    def __init__(self, bus):
        self.__run_cmd('modprobe i2c-dev')
        self.__bus = bus
        self.__real_bus = -1

    def __del__(self):
        try:
            os.unlink(self.__bus_link)
            cmd = 'modprobe -r i2c-stub'
            self.__run_cmd(cmd)
        except:
            # ignore errors
            pass

    def __str__(self):
        if self.__bus_link:
            return self.__bus_link
        return ''

    def bus(self):
        return self.__bus

    def real_bus(self):
        return self.__real_bus

    def add_fake_devices(self, devices_list):
        list_addr = ','.join(map(hex, devices_list))
        cmd = 'modprobe i2c-stub chip_addr=' + list_addr
        self.__run_cmd(cmd)
        self.__symlink_i2c_stub()

    def __run_cmd(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return result.returncode, result.stdout.decode(), result.stderr.decode()

    def __symlink_i2c_stub(self):
        output = self.__run_cmd('i2cdetect -l')
        i2c_bus = ''
        for line in output[1].split('\n'):
            if 'SMBus stub driver' in line:
                i2c_bus = line.split()[0]
                self.__real_bus = int(i2c_bus.strip('i2c-'))

        self.__bus_link = '/dev/i2c-' + str(self.__bus)
        os.symlink('/dev/' + i2c_bus, self.__bus_link)


fake_i2c_bus = FakeI2c(113)
fake_i2c_bus.add_fake_devices([0x11, 0x12, 0x15])

import time
while True:
    time.sleep(1)
