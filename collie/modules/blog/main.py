# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/17 0017.
from collie.core.app import CollieModule
from collie.ext.security import check_token
from flask_restful import Api
from .restful import HomeResource, PostResource, TagResource, CommentResource

module = CollieModule('blog', __name__, url_prefix='/api/blog')
module.before_request(check_token)
api = Api(module)

api.add_resource(HomeResource, '/')
api.add_resource(PostResource, '/post/')
api.add_resource(TagResource, '/tag/')
api.add_resource(CommentResource, '/comment/')
