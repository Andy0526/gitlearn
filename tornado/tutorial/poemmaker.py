# -*- coding: utf-8 -*-
# author:lewsan

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options


def make_parser():
    define('port', default=8000, type=int, help='run on the given port')


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class PoemPageHandler(tornado.web.RequestHandler):

    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render(
            'poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)


def initialize_handlers():
    handlers = [
        (r'/', IndexHandler),
        (r'/poem', PoemPageHandler),
    ]
    return handlers


def initialize_app():
    handlers = initialize_handlers()
    app = tornado.web.Application(
        handlers=handlers,
        template_path=os.path.join(os.path.dirname(__file__), "templates")
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
# import os.path
#
# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
# import tornado.web
#
# from tornado.options import define, options
#
# define("port", default=8000, help="run on the given port", type=int)
#
#
# class IndexHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render('index.html')
#
#
# class PoemPageHandler(tornado.web.RequestHandler):
#     def post(self):
#         noun1 = self.get_argument('noun1')
#         noun2 = self.get_argument('noun2')
#         verb = self.get_argument('verb')
#         noun3 = self.get_argument('noun3')
#         self.render('poem.html', roads=noun1, wood=noun2, made=verb,
#                     difference=noun3)
#
#
# if __name__ == '__main__':
#     tornado.options.parse_command_line()
#     app = tornado.web.Application(
#         handlers=[(r'/', IndexHandler), (r'/poem', PoemPageHandler)],
#         template_path=os.path.join(os.path.dirname(__file__), "templates")
#     )
#     http_server = tornado.httpserver.HTTPServer(app)
#     http_server.listen(options.port)
#     tornado.ioloop.IOLoop.instance().start()
