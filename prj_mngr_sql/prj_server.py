#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from mimetypes import types_map
from prj_model import User


def get_content(self, path, data={}):
    try:
        if self.path == path:
            self.path = "app/index.html"

        fname, ext = os.path.splitext(self.path)

        if ext in (".html", ".css", ".js"):
            if 'index' in fname:
                f = open(os.curdir + os.sep + self.path)
                response = bytes(f.read().replace("$message$", data['message']), "utf8")
            else:
                f = open('app/' + os.curdir + os.sep + self.path)
                response = bytes(f.read(), "utf8")
        elif ext in (".png", ".jpg"):
            f = open('app/' + os.curdir + os.sep + self.path, 'rb')
            response = f.read()
        else:
            response = bytes('', "utf8")

        self.send_response(200)
        self.send_header('Content-type', types_map[ext])
        self.end_headers()
        self.wfile.write(response)
        return

    except IOError:
        self.send_error(404)


def get_request_data(self):
    content_len = int(self.headers.get('content-length', 0))
    post_body = self.rfile.read(content_len)
    data = {d.split('=')[0]: d.split('=')[1] for d in str(post_body, 'utf-8').split('&')}
    return data


# HTTPRequestHandler class
class Server(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        get_content(self, "/", {'message': ''})

    def do_POST(self):
        data = get_request_data(self)

        if data['submit'] == 'login':
            get_content(self, "/", data={'message': 'Invalid'})

def run():
    print('starting server...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, Server)
    print('running server...')
    httpd.serve_forever()


run()


'''
if data:
    self.send_response(200)
    self.send_header('Content-type', types_map[ext])
    self.end_headers()
    self.wfile.write(bytes(f.read().replace("$message$", data['message']), "utf8"))
    return
'''