# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/16 0016.
from flask import jsonify


def res_error(msg=None, status="error"):
    res = {
        "status": status,
        "message": msg
    }
    return jsonify(res)


def res_success(msg=None, data={}, status="success"):
    res = {
        "status": status,
        "message": msg,
        "data": data
    }
    return jsonify(res)
