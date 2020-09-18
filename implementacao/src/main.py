#!/usr/bin/env python3

import os
import sys
import time
import json
import getopt
import signal
import datetime
import threading

import warnings
# Don't show twisted warn
warnings.simplefilter("ignore")
from twisted.internet import reactor, protocol
from twisted.protocols import policies

import devices
import config

stop = False
config_file = 'config.json'

class TcpServer(protocol.Protocol, policies.TimeoutMixin):
    def connectionMade(self):
        self.setTimeout(5)

    def dataReceived(self, data):
        data_dec = data.decode()

        # Devices infos
        if 'i?\n' in data_dec:
            data_dec = data_dec.replace('i?\n', '')
            devs_read = devices.devices.read()
            data_send = 'i:' + json.dumps(devs_read) + '\n'
            self.transport.write(data_send.encode())

        # ULR server
        if 's?\n' in data_dec:
            data_dec = data_dec.replace('s?\n', '')
            data_send = 's:' + config.config["server"]["url"] + '\n'
            self.transport.write(data_send.encode())

        # Local date
        if 'd?\n' in data_dec:
            data_dec = data_dec.replace('d?\n', '')
            data_send = 'd:' + str(datetime.date.today()) + '\n'
            self.transport.write(data_send.encode())

        # Local time
        if 't?\n' in data_dec:
            data_dec = data_dec.replace('t?\n', '')
            now = datetime.datetime.now()
            data_send = 't:' + now.strftime('%H:%M:%S') + '\n'
            self.transport.write(data_send.encode())

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

        self.transport.loseConnection()

    def parse(self, opt, data):
        start = data.find(opt)
        end = data[start:].find('\n') + start
        if end > start + len(opt):
            return data[start + len(opt):end], start, end
        return '', -1, -1


def run(config):
    devices.init(config)
    interval = config['server']['send_interval']
    now = time.time()
    old = now - interval
    while not stop:
        now = time.time()
        if now - old >= interval:
            print(devices.devices.read())
            old = now
        time.sleep(1)


def main(prog_name, argv):
    global config_file
    try:
        opts, _ = getopt.getopt(argv, 'hc:', ['config_file='])
    except getopt.GetoptError:
        print(prog_name + ' -c <config_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(prog_name + ' -c <config_file>')
            sys.exit()
        elif opt in ('-c', '--config_file'):
            config_file = arg

    if not config.read_file(config_file):
        print('Error in read config file. Using default params.')

    thread = threading.Thread(target=run, args=(config.config,))
    thread.start()

    signal.signal(signal.SIGINT, lambda *a: reactor.stop())

    factory = protocol.ServerFactory()
    factory.protocol = TcpServer
    reactor.listenTCP(config.config['tcp_port'], factory)
    reactor.run()
    print('stopping...')
    global stop
    stop = True
    thread.join()


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
