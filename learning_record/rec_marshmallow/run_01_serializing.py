# -*- coding: utf-8 -*-

"""Serializing（序列化）

1）序列化的方法:
    dump()  方法实现 obj -> dict ;
    dumps() 方法实现 obj -> string【json】.

    由于 Flask 能直接序列化 dict（使用 jsonify ），而且你肯定还会对 dict 进一步处理，没必要现在转化成string，
    故通常 Flask 与 Marshmallow 配合序列化时，用 dump()方法即可。


2）过滤输出（过滤出schema定义的字段中你想要的个别字段）:
    only        参数来指定你 需要 输出的字段，
    exclude     参数来排除你 不想 输出的字段。

"""

if __name__ == '__main__':
    from marshmallow import pprint
    from learning_record.rec_marshmallow.models import User
    from learning_record.rec_marshmallow.schemas import UserSchemaN01

    user = User(name="Monty", email="monty@python.org")
    schema = UserSchemaN01()
    result = schema.dump(user)

    data, errors = result  # -------------------> 判断数据验证的结果会用到 errors
    pprint(data)
    print type(data)
    pprint(errors)
    print type(errors)
    # {
    # "name": "Monty",
    # "email": "monty@python.org",
    # "created_at": "2019-03-12T14:46:20.197156+00:00"
    # }
    # <type 'dict'>
    # {}
    # <type 'dict'>

    print '\n---------------- 过滤输出 ----------------\n'

    summary_schema = UserSchemaN01(only=('name', 'email'))
    res = summary_schema.dump(user).data
    pprint(res)
    # {"name": "Monty Python", "email": "monty@python.org"}

    summary_schema_2 = UserSchemaN01(exclude=('email', ))
    res_2 = summary_schema_2.dump(user).data
    pprint(res_2)
    # {u'created_at': '2019-03-12T15:00:55.303128+00:00', u'name': u'Monty'}
