import json
import logging
import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

logger = logging.getLogger("ontkyc")

define("port", default=8801, help="run on the default port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    """Use to test."""
    def get(self):
        self.write("Hello, ONT&COT KYC!")


class NotifyHandler(tornado.web.RequestHandler):
    """
    回调函数，接收证书信息.
    """
    def post(self):
        logger.info(
            "Notify/begin......, client_ip={}, arguments={}".format( self.request.remote_ip, self.request.arguments)
        )
        logger.info(
            "Notify/body..., body_arguments={}, body={}".format(self.request.body_arguments, self.request.body)
        )
        jsonData = json.loads(self.request.body)
        logger.info(
            "Notify/json_data..., jsonData={}".format(jsonData)
        )

        for k, v in self.request.body_arguments.items():
            logger.info("Notify/body_item..., k={}, v={}/{}".format( k, type(v), v))

        # 应答.
        respon = {
            'Action' :  'AuthConfirm',
            "Error": 0,
            "Desc": "SUCCESS",
            "Result": 'true',
        }
        responJson = tornado.escape.json_encode(respon)
        self.write(responJson)


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

