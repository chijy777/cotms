import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.httpserver import HTTPServer


define("port", default=8801, help="run on the default port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    """Use to test."""
    def get(self):
        self.write("Hello, ONT&COT KYC!")


class NotifyHandler(tornado.web.RequestHandler):
    def post(self):
        print("ip============>", self.request.remote_ip)
        uname = self.get_argument('username')
        print("user============>", uname)
        pwd = self.get_argument('password')
        print("pwd============>", pwd)
        respon = {'return': uname}
        respon_json = tornado.escape.json_encode(respon)
        self.write(respon_json)

application = tornado.web.Application([
    (r"/ontkyc", IndexHandler),
    (r"/ontkyc/notify", NotifyHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print('Server running on http://0.0.0.0:%d' % (options.port))
    tornado.ioloop.IOLoop.instance().start()

