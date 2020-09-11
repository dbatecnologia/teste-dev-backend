#!/usr/bin/env python3

import os
import pty

class FakeSerial:
    """
    Fake Serial class.
    """

    def __init__(self, port):
        self.__port = port
        self.__master = None
        self.__slave = None

    def __del__(self):
        #self.close()
        None

    def __str__(self):
        return self.port()

    def open(self):
        self.__master, self.__slave = pty.openpty()
        os.symlink(self.pty(), self.port())

    def close(self):
        os.unlink(self.__port)
        os.close(self.__master)
        self.__master = None
        self.__slave = None

    def write(self, data):
        # string needs to be converted byte object
        b = str.encode(data)
        # returns the number of bytes written in the serial
        return os.write(self.__master, b)

    def read(self):
        # TODO
        None

    def port(self):
        return self.__port

    def pty(self):
        pty_name = os.ttyname(self.__slave)
        return pty_name
