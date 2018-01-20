# -*- coding: utf-8 -*-
# author:lewsan

import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import options, define


def make_parser():
    define('port', default=8000, type=int, help='run the given port')


class MainHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render(
            'index.html',
            page_title="Burt's Books | Home",
            header_text="Welcome to Burt's Books!",
        )


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def makeup_server():
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)


def run():
    makeup_server()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    make_parser()
    run()
