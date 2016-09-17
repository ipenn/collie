#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/7 0007.
import logging
import click
from collie import create_app

app = create_app()


@click.group()
def core_cmd():
    """ Core commands"""
    pass


@core_cmd.command()
@click.option('--reloader/--no-reloader', default=True)
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def runserver(reloader, debug, host, port):
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)


@core_cmd.command()
@click.option('--debug/--no-debug', default=True)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=5000)
def gevent_server(debug, host, port):
    import gevent.monkey
    gevent.monkey.patch_all()
    from gevent.wsgi import WSGIServer
    app.debug = debug
    server = WSGIServer((host, port), application=app)
    server.serve_forever()




help_text = """..."""
manager = click.CommandCollection(help=help_text)
manager.add_source(core_cmd)

if __name__ == '__main__':
    manager()
