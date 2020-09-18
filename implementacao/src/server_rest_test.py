import tornado.ioloop
import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        print('==================')
        print(self.request)
        print(self.request.body.decode())

def make_app():
    return tornado.web.Application([
        (r"/api/v1.0/devices/.*", HelloHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
