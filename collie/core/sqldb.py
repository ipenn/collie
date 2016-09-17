# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/8 0008.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def config(app):
    db.init_app(app)
    db.app = app
    db.create_all()
