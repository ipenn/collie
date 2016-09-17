# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/8 0008.
from flask import render_template
from flask_security import Security as _Security, MongoEngineUserDatastore
from flask_security.forms import RegisterForm, Required
from wtforms import StringField
from collie.modules.accounts.models import Role, User
from pprint import pprint
from flask_security.decorators import _check_token


def check_token():
    _check_token()


class Security(_Security):
    def render_template(self, *args, **kwargs):
        return render_template(*args, **kwargs);


class ExtendedRegisterForm(RegisterForm):
    name = StringField('name', [Required()])


def configure(app, db):
    register_form = ExtendedRegisterForm
    confirm_register_form = ExtendedRegisterForm
    Security(
        app=app,
        datastore=MongoEngineUserDatastore(db, User, Role),
        register_form=register_form,
        confirm_register_form=confirm_register_form

    )
