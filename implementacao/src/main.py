#!/usr/bin/env python3

import sys
import time
import getopt
import threading

import devices
import config
import rest_api
import config_server

stop = False
config_file = 'config.json'


def run(config):
    devices.init(config)
    interval = config['server']['send_interval']
    now = time.time()
    old = now - interval
    while not stop:
        now = time.time()
        if now - old >= interval:
            old = now
            url = config['server']['url']
            data = devices.devices.read()
            rest_api.send(url, data)
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

    config_server.run()
    print('stopping...')
    global stop
    stop = True
    thread.join()


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
