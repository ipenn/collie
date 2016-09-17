# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/16 0016.
from flask_restful import Resource
from flask import url_for, jsonify


class HomeResource(Resource):
    def get(self):
        data = {
            'hello': 'blog!'
        }
        return jsonify(data)
