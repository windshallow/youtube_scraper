# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


class UserSchemaN01(Schema):
    """仅需要这三个字段"""
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()  # 序列化时自动生成该值
