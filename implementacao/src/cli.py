#!/usr/bin/env python3

import sys
import json
import getopt
import datetime

import warnings
# Don't show twisted warn
warnings.simplefilter("ignore")
from twisted.internet import reactor, protocol


class TcpClient(protocol.Protocol, protocol.ClientFactory):
    protocol = None
    opts = ''
    def connectionMade(self):
        self.transport.write(self.opts.encode())

    def dataReceived(self, data):
        data_list = data.decode().split('\n')
        for item in data_list:
            item = item[item.find(':') + 1:]
            try:
                parsed = json.loads(item)
                print(json.dumps(parsed, indent=4, sort_keys=True))
            except:
                print(item)
        self.transport.loseConnection()

    def connectionLost(self, reason):
        pass

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()


def print_help(prog_name):
    print('Usage: ' + prog_name + ' <opt [arg]>')
    print('opt:')
    print('\t-h: show this help')
    print('\t-i: show devices informations')
    print('\t-s: show url server')
    print('\t-t: show current time')
    print('\t-d: show current date')
    print('\t-u [server]: change server')
    print('\t-n [time hh:mm:ss]: change current time')
    print('\t-m [date aaaa-mm-dd]: change current date')

def main(prog_name, argv):
    try:
        opts, _ = getopt.getopt(argv, 'histdu:n:m:',
                ['server=', 'time=', 'date='])
    except getopt.GetoptError:
        print_help(prog_name)
        sys.exit(2)

    if len(opts) == 0:
        print_help(prog_name)

    opts_tcp = ''

    for opt, arg in opts:
        if opt == '-h':
            print_help(prog_name)
            sys.exit()
        elif opt == '-i':
            opts_tcp += 'i?\n'
        elif opt == '-s':
            opts_tcp += 's?\n'
        elif opt == '-t':
            opts_tcp += 't?\n'
        elif opt == '-d':
            opts_tcp += 'd?\n'
        elif opt in ('-u', '--server'):
            opts_tcp += 'u:' + arg + '\n'
        elif opt in ('-n', '--time'):
            opts_tcp += 'n:' + arg + '\n'
        elif opt in ('-m', '--date'):
            opts_tcp += 'm:' + arg + '\n'

    f = TcpClient()
    f.protocol = TcpClient
    f.protocol.opts = opts_tcp
    reactor.connectTCP("localhost", 1234, f)
    reactor.run()

if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
