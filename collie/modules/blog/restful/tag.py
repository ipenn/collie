# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/17 0017.
from flask_restful import Resource, reqparse, inputs
from ..models import Tag
from .utils import res_success, res_error


class TagResource(Resource):
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
            data_list = list()
            data_paginate = Tag.objects(**search).paginate(page=args.get('page'), per_page=args.get('per_page'))
            for tag in data_paginate.items:
                res = self.tag_parse(tag)
                data_list.append(res)

            data = dict()
            data["tag_list"] = data_list
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
            tag = Tag.objects(id=_id).first()
            if tag is None:
                return res_error(msg="Can not find tag")
            data = self.tag_parse(tag)
            return res_success(data=data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        parser.add_argument('description', required=True, help='description is required')
        args = parser.parse_args()

        tag = Tag(**args)
        try:
            tag.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.tag_parse(tag)
        return res_success(data=data)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        parser.add_argument('name')
        parser.add_argument('description')
        args = parser.parse_args()

        tag = Tag.objects(id=args.get('id')).first()
        if tag is None:
            return res_error(msg='Can not find tag')

        try:
            tag.save()
        except Exception as e:
            return res_error(msg=str(e))
        data = self.tag_parse(tag)
        return res_success(data=data)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='id is required')
        args = parser.parse_args()

        tag = Tag.objects(id=args.get('id')).first()
        if tag is None:
            return res_error(msg="Can not find tag")
        tag.delete()
        data = self.tag_parse(tag)
        return res_success(data=data)

    def tag_parse(self, tag):
        res = tag.to_mongo().to_dict()
        _id = str(res.get('_id'))
        res.pop('_id')
        res['id'] = _id
        return res
