# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/17 0017.
from collie.core.db import db
from mongoengine import fields, queryset_manager
import mongoengine


class Tag(db.Document):
    name = fields.StringField(max_length=80, required=True, unique=True)
    description = fields.StringField(max_length=255)

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.description)


class Post(db.Document):
    title = fields.StringField(max_length=255, required=True)
    create_at = fields.DateTimeField()
    tag = fields.ListField(
        fields.ReferenceField(Tag, reverse_delete_rule=mongoengine.DENY), default=[]
    )
    article = fields.StringField()
    url = fields.StringField()

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('-create_at')

    def __unicode__(self):
        return u"{0}".format(self.title)


class Comment(db.Document):
    post = fields.ReferenceField(Post, reverse_delete_rule=mongoengine.CASCADE)
    name = fields.StringField(80)
    email = fields.StringField(255)
    content = fields.StringField(1000)
    create_at = fields.DateTimeField()

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('-create_at')

    def __unicode__(self):
        return u"{0} ({1})".format(self.post.title, self.name)
