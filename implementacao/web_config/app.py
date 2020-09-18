#!/usr/bin/env python3
#
# References:
#  Tornado User Authentication Example
#   (https://github.com/mehmetkose/tornado-user-authentication-example)

import json
import socket

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
from tornado.options import define, options

define('port', default=8888, help='run on the given port', type=int)

server = None
date = None
time = None
devices = None

def get_data(data):
    HOST = '127.0.0.1'
    PORT = 1234
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send(data.encode())
    data = tcp.recv(1024)
    tcp.close()

    global devices
    global date
    global time
    global server
    data_list = data.decode().split('\n')
    for item in data_list:
        if item.find('i:') >= 0:
            item = item[item.find('i:') + 2:]
            try:
                devices = json.loads(item)
            except Exception as e:
                print('Error: ', repr(e))
        if item.find('s:') >= 0:
            server = item[item.find(':') + 1:]
        if item.find('d:') >= 0:
            date = item[item.find(':') + 1:]
        if item.find('t:') >= 0:
            time = item[item.find(':') + 1:]

def set_data(data):
    HOST = '127.0.0.1'
    PORT = 1234
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send(data.encode())
    tcp.close()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

class SettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        get_data('s?\nd?\nt?\n')
        self.render('settings.html', server=server, date=date, time=time)

    @tornado.gen.coroutine
    def post(self):
        incorrect = self.get_secure_cookie('incorrect')
        if incorrect and int(incorrect) > 20:
            self.write('<center>blocked</center>')
            return

        server = tornado.escape.xhtml_escape(self.get_argument('server'))
        data = 'u:' + server + '\n'
        date = tornado.escape.xhtml_escape(self.get_argument('date'))
        try:
            change_date = tornado.escape.xhtml_escape(self.get_argument('change_date'))
            data += 'm:' + date + '\n'
        except:
            pass
        time = tornado.escape.xhtml_escape(self.get_argument('time'))
        try:
            change_time = tornado.escape.xhtml_escape(self.get_argument('change_time'))
            data += 'n:' + time + '\n'
        except:
            pass

        set_data(data)
        self.render('settings.html', server=server, date=date, time=time)


class DevicesHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        get_data('i?\n')
        self.render('devices.html',
                distance     = devices['distance'],
                luminosity   = devices['light'],
                battery      = devices['battery'],
                lighting     = False,
                gps_lat      = devices['gps']['latitude'],
                gps_lat_dir  = devices['gps']['latitude_direction'],
                gps_lon      = devices['gps']['longitude'],
                gps_lon_dir  = devices['gps']['longitude_direction'],
                gprs         = devices['gprs_connection'])


class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        incorrect = self.get_secure_cookie('incorrect')
        if incorrect and int(incorrect) > 20:
            self.write('<center>blocked</center>')
            return
        self.render('login.html')

    @tornado.gen.coroutine
    def post(self):
        incorrect = self.get_secure_cookie('incorrect')
        if incorrect and int(incorrect) > 20:
            self.write('<center>blocked</center>')
            return

        getusername = tornado.escape.xhtml_escape(self.get_argument('username'))
        getpassword = tornado.escape.xhtml_escape(self.get_argument('password'))
        if 'admin' == getusername and 'admin' == getpassword:
            self.set_secure_cookie('user', self.get_argument('username'))
            self.set_secure_cookie('incorrect', '0')
            self.redirect(self.reverse_url('main'))
        else:
            incorrect = self.get_secure_cookie('incorrect') or 0
            increased = str(int(incorrect)+1)
            self.set_secure_cookie('incorrect', increased)
            self.write("""<center>
                            Something Wrong With Your Data (%s)<br />
                            <a href="/">Go Home</a>
                          </center>""" % increased)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', self.reverse_url('main')))

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            'cookie_secret': 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
            'login_url': '/login',
            'template_path': os.path.join(base_dir, 'templates'),
            'static_path': os.path.join(base_dir, 'static'),
            'debug':True,
            'xsrf_cookies': True,
        }

        tornado.web.Application.__init__(self, [
            tornado.web.url(r'/', DevicesHandler, name='main'),
            tornado.web.url(r'/devices', DevicesHandler, name='devices'),
            tornado.web.url(r'/settings', SettingsHandler, name='settings'),
            tornado.web.url(r'/login', LoginHandler, name='login'),
            tornado.web.url(r'/logout', LogoutHandler, name='logout'),
        ], **settings)

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
