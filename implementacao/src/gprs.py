#!/usr/bin/env python3

import serial

class Gprs:
    def __init__(self, port='/dev/ttyACM200', bps=9600):
        self.__serial = serial.Serial()
        self.__serial.port = port
        self.__port = port
        self.__bps = bps

    def open_connection(self, apn):
        try:
            self.__serial.open()
        except:
            return False

        # Enable echo.
        if self.__write_at_cmd('ATE1\r\n') is False:
            self.__serial.close()
            return False

        # Deregister from network.
        if self.__write_at_cmd('AT+COPS=2\r\n') is False:
            self.__serial.close()
            return False

        # Set network to automatic.
        if self.__write_at_cmd('AT+COPS=0\r\n') is False:
            self.__serial.close()
            return False

        # Set APN
        at = 'AT+CGDCONT=1,"IP","' + apn + '","",0,0\r\n'
        if self.__write_at_cmd(at) is False:
            self.__serial.close()
            return False

        self.__serial.close()
        return True

    def is_connected(self):
        try:
            self.__serial.open()
            at = 'AT+CGREG?\r\n'
            self.__serial.write(at.encode())
        except:
            self.__serial.close()
            return False
        ret, lines = self.__read_at_ok_or_error()
        self.__serial.close()
        if ret != 0:
            return False

        lines = ''.join(lines)
        if '+CGREG:' not in lines:
            return False
        try:
            i = lines.find('+CGREG:') + len('+CGREG:')
            lines = lines[i:]
            i = lines.find('\r')
            if int(lines[:i]) == 0:
                return False
        except:
            return False
        return True

    def __write_at_cmd(self, cmd):
        try:
            size = self.__serial.write(cmd.encode())
        except:
            return False
        if size != len(cmd):
            return False
        ret, lines = self.__read_at_ok_or_error()
        if ret != 0:
            return False
        return True

    def __read_at_ok_or_error(self):
        """
        Read until OK or ERROR.
        0: 'OK'
        1: 'ERROR'
        2: Cannot read 'OK' or 'ERROR'
        """
        ret = 2
        lines = list()
        for _ in range(10):
            try:
                data = self.__serial.readline().decode()
            except:
                ret = 2
                break
            lines.append(data)
            if 'OK' in data:
                ret = 0
                break
            if 'ERROR' in data:
                ret = 1
                break
        return ret, lines
