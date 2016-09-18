# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/16 0016.
from pprint import pprint
from faker import Factory, Faker
from collie import create_app_min
from collie.modules.accounts.models import Role, User

app = create_app_min()
fake_zh = Factory.create('zh_CN')
fake = Faker()


def create_roles():
    for _ in range(0, 100):
        fake.seed(_)
        # fake_zh.seed(_)
        # data = {
        #     "name": fake.word(),
        #     "description": fake_zh.sentence(nb_words=6)
        # }
        # pprint(data)
        name = fake.name()
        test = Role.objects(name=name).first()
        pprint(test)
        if test is None:
            role = Role()
            role.name = name
            role.description = fake.sentence(nb_words=6)
            role.save()


def create_users():
    role = Role.objects(id='57dbfd6ae138234da28d6158').first()
    for _ in range(0, 100):
        fake.seed(_)
        fake_zh.seed(_)
        name = fake_zh.name()
        email = fake.email()
        password = fake.password()
        user = User()
        user.active = False
        user.email = email
        user.name = name
        user.password = password
        user.roles = [role]
        try:
            user.save()
        except Exception as e:
            pprint(e)


if __name__ == '__main__':
    # create_users()
    for _ in range(0, 100):
        pprint(fake.password())