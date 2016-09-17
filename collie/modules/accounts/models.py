# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/8 0008.
import logging
from collie.core.db import db
from mongoengine import fields
import mongoengine
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timedelta


logger = logging.getLogger()


# Auth
class Role(db.Document, RoleMixin):
    name = fields.StringField(max_length=80, unique=True)
    description = fields.StringField(max_length=255)

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.description or 'Role')


class User(db.Document, UserMixin):
    name = fields.StringField(max_length=255)
    email = fields.StringField(max_length=255, unique=True)
    password = fields.StringField(max_length=255)
    active = fields.BooleanField(default=True)
    confirmed_at = fields.DateTimeField()
    roles = fields.ListField(
        fields.ReferenceField(Role, reverse_delete_rule=mongoengine.DENY), default=[]
    )
    last_login_at = fields.DateTimeField()
    current_login_at = fields.DateTimeField()
    last_login_ip = fields.StringField(max_length=255)
    current_login_ip = fields.StringField(max_length=255)
    login_count = fields.IntField()

    def __unicode__(self):
        return u"{0} <{1}>".format('', self.email)


# OAuth
class Client(db.Document):
    # human readable name, not required
    name = fields.StringField(max_length=40)

    # human readable description, not required
    description = fields.StringField(max_length=500)

    client_id = fields.StringField()
    client_secret = fields.StringField(max_length=55, unique=True, null=False)

    # public or confidential
    client_type = fields.StringField(max_length=20, default='public')
    redirect_uris = fields.ListField(fields.StringField(max_length=255))
    default_scopes = fields.ListField(fields.StringField(max_length=255), default=['email', 'address'])

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'password', 'client_credentials',
                'refresh_token']


class Grant(db.Document):
    client_id = fields.StringField()
    code = fields.StringField()
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    scopes = fields.ListField(fields.StringField())
    expires = fields.DateTimeField()
    redirect_uri = fields.StringField()


class Token(db.Document):
    access_token = fields.StringField()
    refresh_token = fields.StringField()
    client_id = fields.StringField()
    scopes = fields.ListField(fields.StringField())
    expires = fields.DateTimeField()
    user = fields.ReferenceField(User)
