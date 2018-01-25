#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options


def make_parse():
    define("port", default=8099, help="run on the give port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        import traceback
        traceback.print_exc()
        greeting = self.get_argument('greeting', default='Hello')
        print(type(self), self)
        self.write(greeting + ', friendly user!')


if __name__ == '__main__':
    make_parse()
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    task = tornado.ioloop.IOLoop.current()
    print(type(task))
    task.start()
