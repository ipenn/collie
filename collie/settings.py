# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/7 0007.
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# App Config
DEBUG = True
SECRET_KEY = 'super-secret'

# MongoDB Config
MONGODB_DB = 'mydatabase'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# Security Config
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'  # noqa
SECURITY_URL_PREFIX = '/accounts'
SECURITY_PASSWORD_SALT = '6e95b1ed-a8c3-4da0-8bac-6fcb11c39ab4'  # noqa
# SECURITY_EMAIL_SENDER = 'reply@localhost'
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
# Security miscellaneous
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = False
