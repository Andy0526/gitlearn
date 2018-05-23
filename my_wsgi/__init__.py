# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server


def demo_app(environ,start_response):
    from StringIO import StringIO
    stdout = StringIO()
    print >> stdout, "Hello world!"
    print >> stdout
    h = environ.items();
    h.sort()
    for k, v in h:
        print >> stdout, k, '=', repr(v)
    start_response("200 OK", [('Content-Type', 'text/plain')])
    return [stdout.getvalue()]

def main():
    httpd = make_server('', 8000, demo_app)
