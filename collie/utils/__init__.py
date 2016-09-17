# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/7 0007.
def parse_conf_data(data):
    """
    @int @bool @float @json (for lists and dicts)
    strings does not need converters

    export COLLIE_DEFAULT_THEME='material'
    export COLLIE_DEBUG='@bool True'
    export COLLIE_DEBUG_TOOLBAR_ENABLED='@bool False'
    export COLLIE_PAGINATION_PER_PAGE='@int 20'
    export COLLIE_MONGODB_SETTINGS='@json {"DB": "COLLIE_db", "HOST": "mongo"}'
    export COLLIE_ALLOWED_EXTENSIONS='@json ["jpg", "png"]'
    """
    from flask.json import _json as json
    true_values = ('t', 'true', 'enabled', '1', 'on', 'yes')
    converters = {
        '@int': int,
        '@float': float,
        '@bool': lambda value: True if value.lower() in true_values else False,
        '@json': json.loads
    }
    if data.startswith(tuple(converters.keys())):
        parts = data.partition(' ')
        converter_key = parts[0]
        value = parts[-1]
        return converters.get(converter_key)(value)
    return data
