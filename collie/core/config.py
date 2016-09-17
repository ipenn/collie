# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/7 0007.
import os
import logging
from flask.config import Config
from collie.utils import parse_conf_data

logger = logging.getLogger()


class CollieConfig(Config):
    def from_object(self, obj, silent=False):
        try:
            super(CollieConfig, self).from_object(obj)
        except ImportError as e:
            if silent:
                return False
            e.message = 'Unable to load configuration obj (%s)' % e.message
            raise

    def from_envvar_namespace(self, namespace='QUOKKA', silent=False):
        try:
            data = {
                key.partition('_')[-1]: parse_conf_data(data)
                for key, data
                in os.environ.items()
                if key.startswith(namespace)
                }
            self.update(data)
        except Exception as e:
            if silent:
                return False
            e.message = 'Unable to load config env namespace (%s)' % e.message
            raise

    def load_collie_config(self, config=None, mode=None, test=None, **sets):
        self.from_object(config or 'collie.settings')
        mode = mode or 'test' if test else os.environ.get(
            'COLLIE_MODE', 'local')
        self.from_object('collie.%s_settings' % mode, silent=True)
        path = "COLLIE_SETTINGS" if not test else "COLLIETEST_SETTINGS"
        self.from_envvar(path, silent=True)
        self.from_envvar_namespace(namespace='COLLIE', silent=True)
        self.update(sets)
