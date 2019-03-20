# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load, ValidationError, validates

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


class UserSchemaN03(Schema):
    name = fields.String(required=True)
    email = fields.Email()
    age = fields.Integer(
        required=True,
        error_messages={'required': 'Age is required.'}  # 为 required 验证，定制报错信息
    )
    city = fields.String(
        required=True,
        error_messages={'required': {'message': 'City required', 'code': 400}}  # 为 required 验证，定制报错信息
    )


class BandMemberSchema(Schema):
    name = fields.String(required=True)  # required 默认值为 False; required=True 表示该字段必填，用于验证器。
    email = fields.Email()


class ValidatedUserSchema(UserSchemaN01):
    # NOTE: This is a contrived example.
    # You could use marshmallow.validate.Range instead of an anonymous function here
    age = fields.Number(validate=lambda n: 18 <= n <= 40)


def validate_quantity(n):
    if n < 0:
        raise ValidationError('Quantity must be greater than 0.')
    if n > 30:
        raise ValidationError('Quantity must not be greater than 30.')


class ItemSchema(Schema):
    quantity = fields.Integer(validate=validate_quantity)


class ItemSchemaN01(Schema):
    quantity = fields.Integer()

    @validates('quantity')  # 为 quantity 字段添加验证
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError('Quantity must be greater than 0.')
        if value > 30:
            raise ValidationError('Quantity must not be greater than 30.')
