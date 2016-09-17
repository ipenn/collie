# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/16 0016.
from collie import create_app_min
from collie.modules.accounts.models import Role, User
from mongoengine import Q
from pprint import pprint

app = create_app_min()
# user = User()
# user.name = 'sflksdaf'
# user.email = 'dlskajflsdkaj@dlfkjsal.com'
# user.password = 'fsdaf'
# user.roles = []
# # user.save()
# role = Role.objects.first()
# user.roles.append(role)
# user.save()
role = Role.objects(id='57dbfd6ae138234da28d6158').first()
user = User.objects(Q(roles=role) & Q(roles='小'))
pprint(user)