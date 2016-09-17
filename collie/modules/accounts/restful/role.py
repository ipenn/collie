# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/16 0016.
from flask_restful import Resource, reqparse, inputs
from ..models import Role
from .utils import res_success, res_error
from pprint import pprint

class RoleResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        parser.add_argument("search_name")
        parser.add_argument("search_description")
        args = parser.parse_args()

        search = dict()
        if args.get('search_name'):
            search['name__contains'] = args.get('search_name')
        if args.get('search_description'):
            search['description__contains'] = args.get('search_description')

        _id = args.get('id')
        if (_id is None):
            role_list = list()
            role_paginate = Role.objects(**search).paginate(page=args.get('page'), per_page=args.get('per_page'))
            for role in role_paginate.items:
                res = self.role_parse(role)
                role_list.append(res)

            data = dict()
            data["role_list"] = role_list
            data["page_info"] = {
                "has_next": role_paginate.has_next,
                "has_prev": role_paginate.has_prev,
                "next_num": role_paginate.next_num,
                "page": role_paginate.page,
                "pages": role_paginate.pages,
                "per_page": role_paginate.per_page,
                "prev_num": role_paginate.prev_num,
                "total": role_paginate.total,
            }
            return res_success(data=data)
        else:
            role = Role.objects(id=_id).first()
            if role is None:
                return res_error(msg="Can not find role")
            data = self.role_parse(role)
            return res_success(data=data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        parser.add_argument('description', required=True, help='description is required')
        args = parser.parse_args()

        role = Role(**args)
        try:
            role.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.role_parse(role)
        return res_success(data=data)



    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        parser.add_argument('name')
        parser.add_argument('description')
        args = parser.parse_args()

        role = Role.objects(id=args.get('id')).first()
        if role is None:
            return res_error(msg='Can not find role')

        try:
            role.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.role_parse(role)
        return res_success(data=data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        args = parser.parse_args()

        role = Role.objects(id=args.get('id')).first()
        if role is None:
            return res_error(msg="Can not find role")
        role.delete()
        data = self.role_parse(role)
        return res_success(data=data)

    def role_parse(self, role):
        res = role.to_mongo().to_dict()
        _id = str(res.get('_id'))
        res.pop('_id')
        res['id'] = _id
        return res
