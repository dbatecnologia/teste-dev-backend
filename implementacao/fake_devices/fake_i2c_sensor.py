#!/usr/bin/env python3

import time
import threading

class FakeI2cSensor(threading.Thread):
    """
    Fake I2C sensor implementation.
    """
    __thread_lock = threading.Lock()

    def __init__(self, fake_i2c_bus, i2c_addr, i2c_reg, value_list):
        """
        Initialize and start fake i2c sensor thread.
        """
        if len(value_list) == 0:
            raise ValueError('\'value_list\' is empty')
        threading.Thread.__init__(self)
        self.__stop_event = threading.Event()
        self.__fake_i2c_bus = fake_i2c_bus
        self.__i2c_addr = i2c_addr
        self.__i2c_reg = i2c_reg
        self.__value_list = value_list
        self.start()

    def __del__(self):
        self.stop()

    def stop(self):
        """
        Stop thread loop.
        """
        self.__stop_event.set()

    def run(self):
        """
        Thread loop.
        """
        i = 0
        while not self.__stop_event.is_set():
            value = self.__value_list[i]
            i = i + 1 if i < len(self.__value_list) - 1 else 0
            data = [self.__i2c_addr, value, self.__checksum(value)]
            FakeI2cSensor.__thread_lock.acquire()
            self.__fake_i2c_bus.write_i2c_block_data(self.__i2c_addr,
                    self.__i2c_reg, data)
            FakeI2cSensor.__thread_lock.release()
            time.sleep(1)

    def __checksum(self, value):
        """
        Calculates the checksum.
        """
        return (self.__i2c_addr + value) & 0xff
