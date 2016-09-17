# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/15 0015.

from flask.json import JSONEncoder
from datetime import datetime
import calendar
import time


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                time_time = time.mktime(obj.timetuple())
                return int(time_time)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
