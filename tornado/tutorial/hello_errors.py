#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options


def make_parser():
    define('port', default=8000, type=int, help='run on the port')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_arguments('gretting', 'Hello')
        self.write(greeting + ', friendly user!')

    def write_error(self, status_code, **kwargs):
        self.write('Gosh darint, user! You caused a %d error.' % status_code)


if __name__ == '__main__':
    make_parser()
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/", IndexHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
