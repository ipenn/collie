# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/17 0017.
from flask_restful import Resource, reqparse, inputs
from ..models import Post, Tag
from .utils import res_success, res_error
from datetime import datetime
import time


class PostResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument("url")
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        parser.add_argument("search_title")
        parser.add_argument("search_article")
        parser.add_argument("search_tag", type=self.convert_tag, action='append')
        args = parser.parse_args()

        search = dict()
        if args.get('search_title'):
            search['title__contains'] = args.get('search_title')
        if args.get('search_article'):
            search['article__contains'] = args.get('search_article')
        if args.get('search_tag'):
            search['tag'] = args.get('tag')

        _id = args.get('id')

        if args.get('url') is not None:
            post = Post.objects(url=args.get('url')).first()
            if post is None:
                return res_error(msg="Can not find post")
            data = self.post_parse(post)
            return res_success(data=data)

        if (_id is None):
            data_list = list()
            data_paginate = Post.objects(**search).paginate(page=args.get('page'), per_page=args.get('per_page'))
            for post in data_paginate.items:
                res = self.post_parse(post)
                data_list.append(res)

            data = dict()
            data["post_list"] = data_list
            data["page_info"] = {
                "has_next": data_paginate.has_next,
                "has_prev": data_paginate.has_prev,
                "next_num": data_paginate.next_num,
                "page": data_paginate.page,
                "pages": data_paginate.pages,
                "per_page": data_paginate.per_page,
                "prev_num": data_paginate.prev_num,
                "total": data_paginate.total,
            }
            return res_success(data=data)
        else:
            post = Post.objects(id=_id).first()
            if post is None:
                return res_error(msg="Can not find post")
            data = self.post_parse(post)
            return res_success(data=data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help='title is required')
        parser.add_argument('article', required=True, help='article is required')
        parser.add_argument('url', required=True, help='url is required')
        parser.add_argument('tag[]', dest='tag', type=self.convert_tag, action='append')
        parser.add_argument('create_at', type=self.convert_datetime, default=datetime.now())
        args = parser.parse_args()

        post = Post(**args)
        try:
            post.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.post_parse(post)
        return res_success(data=data)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        parser.add_argument('title', required=True, help='title is required')
        parser.add_argument('article', required=True, help='article is required')
        parser.add_argument('url', required=True, help='url is required')
        parser.add_argument('tag[]', dest='tag', type=self.convert_tag, action='append')
        parser.add_argument('create_at', type=self.convert_datetime, default=datetime.now())
        args = parser.parse_args()

        post = Post.objects(id=args.get('id')).first()
        if post is None:
            return res_error(msg='Can not find post')

        for key in args:
            if args.get(key) is not None:
                post[key] = args.get(key)

        try:
            post.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.post_parse(post)
        return res_success(data=data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        args = parser.parse_args()

        post = Post.objects(id=args.get('id')).first()
        if post is None:
            return res_error(msg="Can not find post")
        post.delete()
        data = self.post_parse(post)
        return res_success(data=data)

    def post_parse(self, post):
        res = post.to_mongo().to_dict()
        _id = str(res.get('_id'))
        res.pop('_id')
        res['id'] = _id
        return res

    def convert_tag(self, tag_id):
        tag = Tag.objects(id=tag_id).first()
        if tag is None:
            raise ValueError('role id {0} is error!'.format(tag_id))
        return tag

    def convert_datetime(self, val):
        val = int(val)
        t = time.localtime(val)
        t = time.mktime(t)
        t = datetime.fromtimestamp(t)
        return t
