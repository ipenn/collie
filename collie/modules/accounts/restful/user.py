# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/16 0016.
from flask import request
from flask_restful import Resource, reqparse, inputs
from ..models import User, Role
from .utils import res_success, res_error
from flask_security.utils import encrypt_password
from pprint import pprint
from datetime import datetime
import time
import re


class UserResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        parser.add_argument("search_name")
        parser.add_argument("search_email")
        parser.add_argument("search_roles", type=self.convert_roles)
        args = parser.parse_args()
        _id = args.get('id')

        search = dict()
        if args.get('search_name'):
            search['name__contains'] = args.get('search_name')
        if args.get('search_email'):
            search['email__contains'] = args.get('search_email')
        if args.get('search_roles'):
            pprint(args.get('search_roles'))
            search['roles'] = args.get('search_roles')
        if (_id is None):
            user_list = list()
            paginate = User.objects(**search).paginate(page=args.get('page'), per_page=args.get('per_page'))
            for user in paginate.items:
                res = self.user_parse(user)
                user_list.append(res)

            data = dict()
            data["user_list"] = user_list
            data["page_info"] = {
                "has_next": paginate.has_next,
                "has_prev": paginate.has_prev,
                "next_num": paginate.next_num,
                "page": paginate.page,
                "pages": paginate.pages,
                "per_page": paginate.per_page,
                "prev_num": paginate.prev_num,
                "total": paginate.total,
            }
            return res_success(data=data)
        else:
            user = User.objects(id=_id).first()
            if user is None:
                return res_error(msg="Can not find role")
            data = self.user_parse(user)

            return res_success(data=data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('email', type=self.convert_email, required=True)
        parser.add_argument('password', type=encrypt_password, required=True)
        parser.add_argument('roles[]', dest='roles', type=self.convert_roles, action='append')
        parser.add_argument('active', type=inputs.boolean, required=True)
        args = parser.parse_args()
        if User.objects(email=args.get('email')).first() is not None:
            return res_error(msg='email is not unique')
        user = User(**args)
        try:
            user.save()
            pass
        except Exception as e:
            return res_error(msg=str(e))
        data = self.user_parse(user)
        return res_success(data=data)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        parser.add_argument('name')
        parser.add_argument('email', type=self.convert_email)
        parser.add_argument('password', type=encrypt_password)
        parser.add_argument('roles[]', dest='roles', type=self.convert_roles, action='append')
        parser.add_argument('active', type=inputs.boolean)
        args = parser.parse_args()

        user = User.objects(id=args.get('id')).first()
        if user is None:
            return res_error(msg='Can not find user')

        for key in args:
            if args.get(key) is not None:
                user[key] = args.get(key)
        pprint(args.get('roles'))
        try:
            user.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.user_parse(user)
        return res_success(data=data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        args = parser.parse_args()

        user = User.objects(id=args.get('id')).first()
        if user is None:
            return res_error(msg="Can not find role")

        user.delete()
        data = self.user_parse(user)
        return res_success(data=data)

    def user_parse(self, user):
        res = user.to_mongo().to_dict()
        if res.get('_id'):
            _id = str(res.get('_id'))
            res['id'] = _id
            res.pop('_id')
        res.pop('password')
        res['password'] = '******'
        res['roles'] = [str(role_id) for role_id in res['roles']]
        return res

    def convert_datetime(self, val):
        val = int(val)
        t = time.localtime(val)
        t = time.mktime(t)
        t = datetime.fromtimestamp(t)
        return t

    def convert_roles(self, role_id):
        role = Role.objects(id=role_id).first()
        if role is None:
            raise ValueError('role id {0} is error!'.format(role_id))
        return role

    def convert_email(self, email):
        if re.match(r'^.+@([^.@][^@]+)$', email) != None:
            return email
        else:
            raise ValueError('must be true email!')
