# -*- coding: utf-8 -*-

"""Partial Loading（部分加载 - 指定无需校验的字段）

1）按照 RESTful 架构风格的要求，更新数据使用HTTP方法中的 PUT 或 PATCH 方法:
    使用 PUT 方法时，需要把  完整的  数据全部传给服务器，
    使用PATCH方法时，只需把需要改动的  部分数据  传给服务器即可。

    因此，当使用 PATCH 方法时，由于之前设定的required，传入数据存在无法通过 Marshmallow 数据校验的风险。
    为了避免这种情况，需要借助 Partial Loading 功能。

2）实现 Partial Loadig 只要在 schema 构造器中增加一个 partial 参数即可：

"""
from marshmallow import Schema, fields

if __name__ == "__main__":

    class UserSchema(Schema):
        name = fields.String(required=True)
        age = fields.Integer(required=True)

    data, errors = UserSchema().load({'age': 42}, partial=('name',))  # 指定无需校验的字段
    # OR UserSchema(partial=('name',)).load({'age': 42})
    print data, errors  # => ({'age': 42}, {})
