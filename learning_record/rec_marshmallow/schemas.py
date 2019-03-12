# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load

from learning_record.rec_marshmallow.models import User


class UserSchemaN01(Schema):
    """仅需要这三个字段"""
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()  # 序列化时自动生成该值


class UserSchemaN02(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load  # 定义 load 方法的后处理操作函数
    def make_user(self, data):
        """每次调用 load() 方法时，会按照make_user的逻辑，返回一个User类对象"""
        return User(**data)
