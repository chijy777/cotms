import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class NotifyHandler(tornado.web.RequestHandler):
    def post(self):
        print("ip============>", self.request.remote_ip)
        uname = self.get_argument('username')
        print("user============>", uname)
        pwd = self.get_argument('password')
        print("pwd============>", pwd)
        # data = self.get_argument('username','password')
        # print("data============>", data)
        respon = {'issuccess': uname}
        respon_json = tornado.escape.json_encode(respon)
        self.write(respon_json)

application = tornado.web.Application([
    (r"/ontkyc", MainHandler),
    (r"/ontkyc/notify", NotifyHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

