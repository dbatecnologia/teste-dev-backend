#!/usr/bin/env python3
#
# References:
#  GPS - NMEA sentence information (http://aprs.gids.nl/nmea)
#  NMEA data (http://www.gpsinformation.org/dale/nmea.htm)

import time
import datetime
import threading
from fake_interfaces import fake_serial

class FakeGpsSensor(threading.Thread):
    """
    Fake GPS sensor implementation.
    """

    def __init__(self, port):
        """
        Initialize and start fake gps sensor thread.
        """
        threading.Thread.__init__(self)
        self.__stop_event = threading.Event()
        self.__fake_serial = fake_serial.FakeSerial()
        self.__fake_serial.port = port
        self.__port = port
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
            self.__fake_serial.write(self.__get_gps_data())
            time.sleep(1)
        self.__fake_serial.close()

    def __nmea_checksum(self, msg):
        """
        The checksum field consists of a '*' and two hex digits representing
        an 8 bit exclusive OR of all characters between, but not including,
        the '$' and '*'.
        """
        checksum = 0
        for char in msg:
           checksum ^= ord(char)
        return hex(checksum).upper()[2:]

    def __get_gps_data(self):
        """
        Get GPS data.

        $GPRMC,hhmmss.ss,A,llll.ll,a,yyyyy.yy,a,x.x,x.x,ddmmyy,x.x,a*hh
        1    = UTC of position fix
        2    = Data status (V=navigation receiver warning)
        3    = Latitude of fix
        4    = N or S
        5    = Longitude of fix
        6    = E or W
        7    = Speed over ground in knots
        8    = Track made good in degrees True
        9    = UT date
        10   = Magnetic variation degrees (Easterly var. subtracts from true
               course)
        11   = E or W
        12   = Checksum
        """

        # Get current time in UTC
        now = datetime.datetime.now(datetime.timezone.utc)
        now_time = now.strftime('%H%M%S')
        now_date = now.strftime('%d%m%y')

        gprmc = 'GPRMC,' + now_time + \
                '.00,A,2736.12493,S,04834.61709,W,0.234,,' + now_date + ',,,A'
        gprmc_checksum = self.__nmea_checksum(gprmc)
        msg = '$' + gprmc + '*' + gprmc_checksum + fake_serial.FakeSerial.CRLF \
            + '$GPVTG,,,,,,,,,N*30' + fake_serial.FakeSerial.CRLF + \
            '$GPGGA,140601.00,,,,,0,00,99.99,,,,,,*64' + \
            fake_serial.FakeSerial.CRLF + \
            '$GPGSV,3,1,10,05,34,266,,07,37,125,,08,14,133,18,09,34,049,33*79' \
            + fake_serial.FakeSerial.CRLF + \
            '$GPGLL,,,,,140601.00,V,N*48' + fake_serial.FakeSerial.CRLF

        return msg
