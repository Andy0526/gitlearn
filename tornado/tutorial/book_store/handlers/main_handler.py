#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render(
            'index.html',
            page_title="Burt's Books | Home",
            header_text="Welcome to Burt's Books!",
        )
