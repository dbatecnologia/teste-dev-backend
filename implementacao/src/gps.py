#!/usr/bin/env python3
#
# References:
#  (https://gist.github.com/Lauszus/5785023)

import serial

class Gps:
    def __init__(self, port='/dev/ttyACM100', bps=9600):
        self.__serial = serial.Serial()
        self.__serial.port = port
        self.__port = port
        self.__bps = bps

    def get_position(self):
        try:
            self.__serial.open()
        except:
            return None
        data = self.__read()
        self.__serial.close()
        if data is None:
            return None
        coord = self.__parse(data)
        return coord

    def __read(self):
        """
        Read until GPRMC data.
        0: OK
        1: Cannot read GPRMC data
        """
        data = None
        for _ in range(10):
            try:
                data = self.__serial.readline().decode()
            except:
                break
            if 'GPRMC' in data:
                break
        return data

    def __parse(self, data):
        data = data.split(',')
        lat_str = data[3]
        lng_str = data[5]
        lat = float(lat_str[:2].lstrip('0') + "." + "%.7s" % \
                str(float(lat_str[2:])*1.0/60.0).lstrip("0."))
        lng = float(lng_str[:3].lstrip('0') + "." + "%.7s" % \
                str(float(lng_str[3:])*1.0/60.0).lstrip("0."))
        lat_direction = data[4]
        lng_direction = data[6]
        return lat, lat_direction, lng, lng_direction
