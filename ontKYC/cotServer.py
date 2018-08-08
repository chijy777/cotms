import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.httpserver import HTTPServer

define("port", default=8000, help="run on the given port", type=int)

class App(tornado.web.Application):
    def __init__(self, handlers, **settings):
        tornado.web.Application.__init__(self, handlers, **settings)
        print(111)

application = App(url_handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print('Server running on http://0.0.0.0:%d' % (options.port))
    tornado.ioloop.IOLoop.instance().start()

