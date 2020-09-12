#!/usr/bin/env python3

import os
import pty

class FakeSerialException(Exception):
    """
    Base class for fake serial port related exceptions.
    """
    pass


class FakeSerial:
    """
    Fake Serial port implementation.
    """

    def __init__(self, port=None):
        """\
        Initialize fake serial port object. If a "port" is given, then the port
        will be opened immediately. Otherwise a Serial port object in closed
        state is returned.
        """

        self.is_open = False
        self.__port = port
        self.__master = None
        self.__slave = None
        if port is not None:
            self.open()

    def __del__(self):
        self.close()

    def __str__(self):
        if self.__port:
            return self.port
        return ''

    def open(self):
        """
        Open port with current settings. This may throw a FakeSerialException
        if the port cannot be opened.
        """
        if self.is_open:
            raise FakeSerialException('Port is already open')

        try:
            if (os.path.islink(self.__port) and not
                    os.path.exists(os.readlink(self.__port))):
                os.unlink(self.__port)
        except Exception as e:
            raise FakeSerialException('Cannot open port: ' + repr(e))

        self.__master, self.__slave = pty.openpty()

        try:
            os.symlink(self.pty(), self.__port)
        except Exception as e:
            raise FakeSerialException('Cannot open port: ' + repr(e))
        else:
            self.is_open = True

    def close(self):
        """
        Close port
        """
        try:
            os.unlink(self.__port)
            os.close(self.__master)
        except:
            # ignore errors
            pass
        self.is_open = False
        self.__master = None
        self.__slave = None

    def write(self, data):
        """
        Output the given string over the fake serial port.
        """
        if not self.is_open:
            raise FakeSerialException(
                'Attempting to use a port that is not open')

        # string needs to be converted byte object
        b = str.encode(data)
        try:
            # returns the number of bytes written in the serial
            return os.write(self.__master, b)
        except Exception as e:
            raise FakeSerialException(
                'Cannot write data: ' + str(e))

    def read(self, size=1):
        """
        Read size bytes from the fake serial port. It will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise FakeSerialException(
                'Attempting to use a port that is not open')
        # TODO

    @property
    def port(self):
        """
        Get the current port setting.
        """
        return self.__port

    @port.setter
    def port(self, port):
        """
        Change the port.
        """
        if port is not None and not isinstance(port, str):
            raise ValueError(
                '"port" must be None or a string, not {}'.format(type(port)))
        self.__port = port
        was_open = self.is_open
        if was_open:
            self.close()
        self.__port = port
        if was_open:
            self.open()

    def pty(self):
        """
        Return a string which specifies the terminal device associated with
        fake serial.
        """
        try:
            return os.ttyname(self.__slave)
        except:
            return ''
