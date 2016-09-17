# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/9 0009.
from flask import Flask
from gevent.wsgi import WSGIServer
from gevent.server import StreamServer

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, Gevent!'


def gevent_server():
    app.debug = True
    server = WSGIServer(('0.0.0.0', 5000), application=app)
    server.serve_forever()

def flask_server():
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    flask_server()