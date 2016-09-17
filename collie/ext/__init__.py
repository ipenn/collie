# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/7 0007.
from collie.core.db import db
from . import security, views, blueprints
# from . import oauth
from flask_cors import CORS
from collie.utils.json import CustomJSONEncoder


def configure_extensions(app):
    db.init_app(app)
    security.configure(app, db)
    # oauth.create_server(app)
    # oauth.create_client(app)
    app.json_encoder = CustomJSONEncoder
    views.configure(app)
    blueprints.load_from_folder(app)
    CORS(app)


def configure_extensions_min(app):
    db.init_app(app)
