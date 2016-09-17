# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/7 0007.
from flask import Flask, Blueprint
from collie.core.config import CollieConfig


class Collie(Flask):
    config_class = CollieConfig


class CollieModule(Blueprint):
    def __init__(self, name, *args, **kwargs):
        name = "collie.modules." + name
        super(CollieModule, self).__init__(name, *args, **kwargs)
