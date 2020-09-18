#!/usr/bin/env python3

import sys
import time
import json
import getopt
import signal
import datetime
import threading
from twisted.internet import reactor, protocol
from twisted.protocols import policies

import devices
import config

stop = False

class TcpServer(protocol.Protocol, policies.TimeoutMixin):
    def connectionMade(self):
        self.setTimeout(5)

    def dataReceived(self, data):
        data_dec = data.decode()

        # Devices infos
        if 'i' in data_dec:
            devs_read = devices.devices.read()
            data_send = 'i:' + json.dumps(devs_read) + '\n'
            self.transport.write(data_send.encode())

        # Local date
        if 'd' in data_dec:
            data_send = 'd:' + str(datetime.date.today()) + '\n'
            self.transport.write(data_send.encode())

        # Local time
        if 't' in data_dec:
            now = datetime.datetime.now()
            data_send = 't:' + now.strftime('%H:%M:%S') + '\n'
            self.transport.write(data_send.encode())

        # ULR server
        if 's' in data_dec:
            data_send = 's:' + config.config["server"]["url"] + '\n'
            self.transport.write(data_send.encode())

        self.transport.loseConnection()


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


def main(argv):
    config_file = 'config.json'
    try:
        opts, _ = getopt.getopt(argv, 'hc:', ['config_file='])
    except getopt.GetoptError:
        print('test.py -c <config_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -c <config_file>')
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
    main(sys.argv[1:])
