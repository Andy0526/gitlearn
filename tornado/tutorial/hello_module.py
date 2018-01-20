#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import os.path
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import define, options


def make_parser():
    define('port', default=8000, type=int, help='run on the port')


class HelloHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('hello.html')


class HelloModule(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        return '<h1> Hello world by module</h1>'


def initialize_handlers():
    handlers = [
        (r'/hello', HelloHandler)
    ]
    return handlers


def initialize_app():
    handlers = initialize_handlers()
    app = tornado.web.Application(
        handlers=handlers,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        ui_modules={
            'Hello': HelloModule,
        },
    )
    return app


def make_up_server():
    make_parser()
    tornado.options.parse_command_line()
    app = initialize_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)


def run():
    make_up_server()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
