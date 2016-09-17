# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/15 0015.
from collie.core.app import CollieModule
from collie.ext.security import check_token
from flask_restful import Api
from .restful import HomeResource, RoleResource, UserResource

module = CollieModule('accounts', __name__, url_prefix='/api/accounts')
module.before_request(check_token)
api = Api(module)

api.add_resource(HomeResource, '/')
api.add_resource(RoleResource, '/role/')
api.add_resource(UserResource, '/user/')
