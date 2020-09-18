#!/usr/bin/env python3

import os
import json
import signal
import datetime

import warnings
# Don't show twisted warn
warnings.simplefilter("ignore")
from twisted.internet import reactor, protocol
from twisted.protocols import policies

import config
import devices

class TcpServer(protocol.Protocol, policies.TimeoutMixin):
    def connectionMade(self):
        self.setTimeout(5)

    def dataReceived(self, data):
        data_dec = data.decode()

        data_send = ''

        # Devices infos
        if 'i?\n' in data_dec:
            data_dec = data_dec.replace('i?\n', '')
            devs_read = devices.devices.read()
            data_send += 'i:' + json.dumps(devs_read) + '\n'

        # ULR server
        if 's?\n' in data_dec:
            data_dec = data_dec.replace('s?\n', '')
            data_send += 's:' + config.config["server"]["url"] + '\n'

        # Local date
        if 'd?\n' in data_dec:
            data_dec = data_dec.replace('d?\n', '')
            data_send += 'd:' + str(datetime.date.today()) + '\n'

        # Local time
        if 't?\n' in data_dec:
            data_dec = data_dec.replace('t?\n', '')
            now = datetime.datetime.now()
            data_send += 't:' + now.strftime('%H:%M:%S') + '\n'

        # Change URL server
        if 'u:' in data_dec:
            url, start, end = self.parse('u:', data_dec)
            data_dec = data_dec[:start] + data_dec[end+1:]
            config.config["server"]["url"] = url
            try:
                config.write_file(config_file)
            except Exception as e:
                print('Cannot write server in config file: ' + repr(e))

        # Change date
        if 'm:' in data_dec:
            date, start, end = self.parse('m:', data_dec)
            data_dec = data_dec[:start] + data_dec[end+1:]
            os.system('date +%Y-%m-%d -s "' + date + '"')

        # Change time
        if 'n:' in data_dec:
            time, start, end = self.parse('n:', data_dec)
            data_dec = data_dec[:start] + data_dec[end+1:]
            os.system('date +%T -s "' + time + '"')

        if len(data_send) > 0:
            self.transport.write(data_send.encode())

        self.transport.loseConnection()

    def parse(self, opt, data):
        start = data.find(opt)
        end = data[start:].find('\n') + start
        if end > start + len(opt):
            return data[start + len(opt):end], start, end
        return '', -1, -1


def run():
    signal.signal(signal.SIGINT, lambda *a: reactor.stop())

    factory = protocol.ServerFactory()
    factory.protocol = TcpServer
    reactor.listenTCP(config.config['tcp_port'], factory)
    reactor.run()
