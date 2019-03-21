# -*- coding: utf-8 -*-

""" “Read-only” and “Write-only” Fields

可以指定某些字段只能够dump()或load()

"""
import datetime
from marshmallow import Schema, fields, pprint


class UserSchema(Schema):
    name = fields.Str(load_only=True)  # 该字段只写, 只可以被 load
    password = fields.Str(load_only=True)
    age = fields.Int(dump_only=True)  # 该字段只读, 只可以被 dump
    created_at = fields.DateTime(dump_only=True)


if __name__ == "__main__":
    data_dict_1 = {
        'name': 'Mike',
        'password': 'password',
        'age': 18,
        "created_at": "2019-03-12T14:46:20.197156+00:00"
    }

    data_1, errors_1 = UserSchema().load(data_dict_1)
    pprint(data_1)  # => {'name': u'Mike', 'password': u'password'}

    data_dict_2 = {
        'name': 'Mike',
        'password': 'password',
        'age': 18,
        'created_at': datetime.datetime.now()
    }
    data_2, errors_2 = UserSchema().dump(data_dict_2)
    pprint(data_2)  # => {u'age': 18, u'created_at': '2019-03-21T11:24:18.779717+00:00'}
