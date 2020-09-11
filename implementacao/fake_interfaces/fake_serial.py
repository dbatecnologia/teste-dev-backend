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

    def open(self):
        self.__open_pty()
        self.__link_pty()

    def close(self):
        self.__unlink_pty()
        self.__close_pty()

    def write(self, data):
        # string needs to be converted byte object
        b = str.encode(data)
        # returns the number of bytes written in the serial
        return os.write(self.__master, b)

    def read(self):
        # TODO
        None

    def __open_pty(self):
        self.__master, self.__slave = pty.openpty()

    def __close_pty(self):
        os.close(self.__master)

    def __link_pty(self):
        pty_name = os.ttyname(self.__slave)
        os.symlink(pty_name, self.__port)

    def __unlink_pty(self):
        os.unlink(self.__port)



import time

fake_serial = FakeSerial('/tmp/ttyACM0');
fake_serial.open()

time.sleep(10)
fake_serial.write('teste \x41 \x42')
time.sleep(1)

fake_serial.close()
