# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/8 0008.
from flask import Blueprint
from flask import url_for, send_from_directory
from flask_security import current_user
from flask_security.utils import config_value
from flask_security.decorators import _check_token

bt = Blueprint('home', __name__)


@bt.route('/')
def index():
    _check_token()
    user = current_user
    if user.is_anonymous:
        res = '<p>Hello, World!</p><a href="{0}">{0}</a>'.format(url_for('security.login'))
    else:
        res = '<p>Hello, {1}!</p><a href="{0}">{0}</a>'.format(url_for('security.logout'), user.name)
    return res

def configure(app):
    app.register_blueprint(bt)
    app.route
