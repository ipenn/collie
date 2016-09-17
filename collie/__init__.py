# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/7 0007.
from collie.core.app import Collie
from collie.ext import configure_extensions, configure_extensions_min


def create_app(config=None, test=False, **settings):
    app = Collie('collie')
    app.config.load_collie_config(config=config, test=test, **settings)
    configure_extensions(app)
    return app


def create_app_min(config=None, test=False, **settings):
    app = Collie('collie')
    app.config.load_collie_config(config=config, test=test, **settings)
    configure_extensions_min(app)
    return app
