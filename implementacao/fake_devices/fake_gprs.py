#!/usr/bin/env python3

import time
import threading
import at_cmd_handler
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
        self.__register_at_cmds()
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
        cmd = ''
        while not self.__stop_event.is_set():
            char = self.__fake_serial.read(1)
            cmd += char

            if self.__ate.value == 1:
                # Echo
                self.__fake_serial.write(char)

            if (char != fake_serial.FakeSerial.CR and
                    char != fake_serial.FakeSerial.LF):
                continue

            # Work around. The atcmd module has a bug with double quotes.
            result = self.__parser.process(cmd.replace('"', ''))
            result_str = result.toString()

            if len(result_str) == 0:
                result_str = at_cmd_handler.ATCommandResult(
                        at_cmd_handler.ATCommandResult.OK).toString()

            self.__fake_serial.write(fake_serial.FakeSerial.CRLF + \
                    result_str + fake_serial.FakeSerial.CRLF)
            cmd = ''
        self.__fake_serial.close()

    def __register_at_cmds(self):
        self.__parser = at_cmd_handler.ATParser()

        # ATE0, ATE1
        self.__ate = at_cmd_handler.AtEHandler()
        self.__parser.register('E', self.__ate)

        # AT+COPS
        self.__atcops = at_cmd_handler.AtCopsHandler()
        self.__parser.register('+COPS', self.__atcops);

        # AT+CGDCONT
        self.__atcgdcont = at_cmd_handler.AtCgdcontHandler()
        self.__parser.register('+CGDCONT', self.__atcgdcont);
