#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

import os.path

import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import tornado.escape

from tornado.options import options, define


def make_parser():
    define('port', type=int, default=8000, help='run the given port')


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render(
            'index.html',
            samples=[
                {
                    "title": "Item 1",
                    "description": "Description for item 1"
                },
                {
                    "title": "Item 2",
                    "description": "Description for item 2"
                },
                {
                    "title": "Item 3",
                    "description": "Description for item 3"
                },
            ]
        )


class SimpleModule(tornado.web.UIModule):
    def render(self, sample):
        return self.render_string(
            'modules/sample.html',
            sample=sample
        )

    def html_body(self):
        return "<div class=\"addition\"><p>html_body()</p></div>"

    def embedded_javascript(self):
        return "document.write(\"<p>embedded_javascript()</p>\")"

    def embedded_css(self):
        return ".addition {color: #A1CAF1}"

    def css_files(self):
        return "css/sample.css"

    def javascript_files(self):
        return "js/sample.js"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        setting = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules={"Sample": SimpleModule},
            debug=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **setting)


def main():
    make_parser()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
