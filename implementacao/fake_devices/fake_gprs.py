#!/usr/bin/env python3
#
# References:

import time
import threading
from fake_interfaces import fake_serial

class FakeGprs(threading.Thread):
    """
    Fake GPRS implementation.
    """

    def __init__(self, port):
        """
        Initialize and start fake gprs thread.
        """
        threading.Thread.__init__(self)
        self.__stop_event = threading.Event()
        self.__fake_serial = fake_serial.FakeSerial()
        self.__fake_serial.port = port
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
        self.__fake_serial.open()
        while not self.__stop_event.is_set():
            time.sleep(1)
        self.__fake_serial.close()
