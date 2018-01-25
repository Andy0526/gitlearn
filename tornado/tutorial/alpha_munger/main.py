#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

import os.path
import random

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import define, options


def make_parser():
    define('port', default=8000, type=int, help='run on the given port.')


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class MungedPageHandler(tornado.web.RequestHandler):
    @classmethod
    def map_by_first_letter(cls, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                word_lst = mapped.setdefault(word[0], [])
                word_lst.append(word)
        return mapped

    def post(self, *args, **kwargs):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines, choice=random.choice)


def get_handlers():
    handlers = [
        (r'/', IndexHandler),
        (r'/poem', MungedPageHandler),
    ]
    return handlers


def initialize_application():
    app = tornado.web.Application(
        handlers=get_handlers(),
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static')
    )
    return app


def makeup_server():
    make_parser()
    tornado.options.parse_command_line()
    app = initialize_application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)


def run():
    makeup_server()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
