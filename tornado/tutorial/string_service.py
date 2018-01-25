#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import textwrap
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.options import define, parse_command_line, options
from tornado.ioloop import IOLoop


def make_parse():
    define("port", default=8000, type=int, help='run on the given port')


class ReverseHandler(RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


if __name__ == '__main__':
    make_parse()
    parse_command_line()
    app = Application([
        (r"/reverse/(\w+)", ReverseHandler),
        (r"/wrap", WrapHandler)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    task_queue = IOLoop.instance()
    print(type(task_queue))
    task_queue.start()
