#!/usr/bin/env python3

import sys
import time
import json
import getopt
import signal
import threading
from twisted.internet import reactor, protocol

import devices

devs = None
stop = False

class TcpServer(protocol.Protocol):
    def connectionMade(self):
        print('new connection')
        devs_read = devs.read()
        self.transport.write(json.dumps(devs_read).encode())
        self.transport.loseConnection()

    def dataReceived(self, data):
        self.transport.write(data)


def run(config):
    global devs

    if config is None:
        interval = 30
        devs = devices.Devices()
    else:
        interval = config['server']['send_interval']
        devs = devices.Devices(
                config['i2c_sensors']['bus'],
                [
                    config['i2c_sensors']['light_sensor_addr'],
                    config['i2c_sensors']['distance_sensor_addr'],
                    config['i2c_sensors']['battery_sensor_addr']
                ],
                config['gps']['port'],
                config['gps']['rate'],
                config['gprs']['port'],
                config['gprs']['rate'],
                config['gprs']['apn'])
    now = time.time()
    old = now - interval
    while not stop:
        now = time.time()
        if now - old >= interval:
            print(devs.read())
            old = now
        time.sleep(1)

def check_config_integrity(config):
    """
    Checks the integrity of the configuration file
    """
    if type(config['tcp_port']) is not int:
        return False

    # Server config
    if type(config['server']) is not dict:
        return False
    if type(config['server']['url']) is not str:
        return False
    if type(config['server']['send_interval']) is not int:
        return False

    # I2C sensors config
    if type(config['i2c_sensors']) is not dict:
        return False
    if type(config['i2c_sensors']['bus']) is not int:
        return False
    if type(config['i2c_sensors']['light_sensor_addr']) is not int:
        return False
    if type(config['i2c_sensors']['distance_sensor_addr']) is not int:
        return False
    if type(config['i2c_sensors']['battery_sensor_addr']) is not int:
        return False

    # GPS config
    if type(config['gps']) is not dict:
        return False
    if type(config['gps']['port']) is not str:
        return False
    if type(config['gps']['rate']) is not int:
        return False

    # GPRS config
    if type(config['gprs']) is not dict:
        return False
    if type(config['gprs']['port']) is not str:
        return False
    if type(config['gprs']['rate']) is not int:
        return False
    if type(config['gprs']['apn']) is not str:
        return False

    return True


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

    config = None
    tcp_port = 1234
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        if not check_config_integrity(config):
            print('Error in config file. Using default params.')
        tcp_port = config['tcp_port']
    except:
        print('Error in read config file. Using default params.')

    thread = threading.Thread(target=run, args=(config,))
    thread.start()
    signal.signal(signal.SIGINT, lambda *a: reactor.stop())

    factory = protocol.ServerFactory()
    factory.protocol = TcpServer
    reactor.listenTCP(tcp_port, factory)
    reactor.run()
    print('stopping...')
    global stop
    stop = True


if __name__ == "__main__":
    main(sys.argv[1:])
