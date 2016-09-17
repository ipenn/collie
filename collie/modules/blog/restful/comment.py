# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/17 0017.
from flask_restful import Resource, reqparse, inputs
from ..models import Comment, Post
from .utils import res_success, res_error
from datetime import datetime
import time


class CommentResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        parser.add_argument('post', type=self.convert_post)
        parser.add_argument("search_name")
        parser.add_argument("search_email")
        parser.add_argument("search_content")
        args = parser.parse_args()

        search = dict()
        if args.get('search_name'):
            search['name__contains'] = args.get('search_name')
        if args.get('search_email'):
            search['email__contains'] = args.get('search_email')
        if args.get('search_content'):
            search['content__contains'] = args.get('search_content')

        _id = args.get('id')

        if args.get('post') is not None:
            data_list = list()
            comments = Comment.objects(post=args.get('post'))
            for comment in comments:
                res = self.comment_parse(comment)
                data_list.append(res)
            return res_success(data=data_list)

        if args.get('url') is not None:
            comment = Comment.objects(url=args.get('url')).first()
            if comment is None:
                return res_error(msg="Can not find comment")
            data = self.comment_parse(comment)
            return res_success(data=data)

        if (_id is None):
            data_list = list()
            data_paginate = Comment.objects(**search).paginate(page=args.get('page'), per_page=args.get('per_page'))
            for comment in data_paginate.items:
                res = self.comment_parse(comment)
                data_list.append(res)

            data = dict()
            data["comment_list"] = data_list
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
            comment = Comment.objects(id=_id).first()
            if comment is None:
                return res_error(msg="Can not find comment")
            data = self.comment_parse(comment)
            return res_success(data=data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('post', type=self.convert_post,
                            required=True, help='title is required')
        parser.add_argument('name', required=True, help='name is required')
        parser.add_argument('email', required=True, help='email is required')
        parser.add_argument('content', required=True, help='content is required')
        parser.add_argument('create_at', type=self.convert_datetime, default=datetime.now())
        args = parser.parse_args()

        comment = Comment(**args)
        try:
            comment.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.comment_parse(comment)
        return res_success(data=data)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        parser.add_argument('post', type=self.convert_post, )
        parser.add_argument('name')
        parser.add_argument('email')
        parser.add_argument('content')
        parser.add_argument('create_at', type=self.convert_datetime, default=datetime.now())
        args = parser.parse_args()

        comment = Comment.objects(id=args.get('id')).first()
        if comment is None:
            return res_error(msg='Can not find comment')

        for key in args:
            if args.get(key) is not None:
                comment[key] = args.get(key)

        try:
            comment.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.comment_parse(comment)
        return res_success(data=data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        args = parser.parse_args()

        comment = Comment.objects(id=args.get('id')).first()
        if comment is None:
            return res_error(msg="Can not find comment")
        comment.delete()
        data = self.comment_parse(comment)
        return res_success(data=data)

    def comment_parse(self, comment):
        res = comment.to_mongo().to_dict()
        _id = str(res.get('_id'))
        res.pop('_id')
        res['id'] = _id
        return res

    def convert_post(self, post_id):
        post = Post.objects(id=post_id).first()
        if post is None:
            raise ValueError('role id {0} is error!'.format(post_id))
        return post

    def convert_datetime(self, val):
        val = int(val)
        t = time.localtime(val)
        t = time.mktime(t)
        t = datetime.fromtimestamp(t)
        return t
