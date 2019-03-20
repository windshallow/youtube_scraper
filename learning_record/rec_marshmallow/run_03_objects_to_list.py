# -*- coding: utf-8 -*-

"""many（参数many的使用）

之前的序列化和反序列化，是针对 单个对象 而言的，对于 多个对象 的处理，只需在schema中增加一个参数：many=True，即：

"""
from marshmallow import pprint

from learning_record.rec_marshmallow.models import User
from learning_record.rec_marshmallow.schemas import UserSchemaN01, UserSchemaN02

if __name__ == '__main__':
    user1 = User(name="Mick", email="mick@stones.com")
    user2 = User(name="Keith", email="keith@stones.com")
    users = [user1, user2]

    print '\n---------------- dump many ----------------\n'

    # option 1:
    schema = UserSchemaN01(many=True)
    result = schema.dump(users)

    data, errors = result
    pprint(data)  # list[dict]
    pprint(errors)  # <type 'dict'>

    print '\n---------------- dump many Option 2 ----------------\n'

    # Option 2:
    schema = UserSchemaN02()
    result = schema.dump(users, many=True)

    data, errors = result
    pprint(data)
    pprint(errors)

    # [{u'created_at': '2019-03-12T16:19:20.653453+00:00',
    #   u'email': u'mick@stones.com',
    #   u'name': u'Mick'},
    #  {u'created_at': '2019-03-12T16:19:20.653463+00:00',
    #   u'email': u'keith@stones.com',
    #   u'name': u'Keith'}]

    print '\n---------------- dumps many ----------------\n'

    schema = UserSchemaN02()
    json_res = schema.dumps(users, many=True).data  # json 字符串
    pprint(json_res)
    # '[{"created_at": "2019-03-12T16:22:47.657290+00:00", "name": "Mick", "email": "mick@stones.com"},
    # {"created_at": "2019-03-12T16:22:47.657300+00:00", "name": "Keith", "email": "keith@stones.com"}]'

    print '\n---------------- load many ----------------\n'

    user_data_s = [
        {
            # 'created_at': '2019-03-12T16:35:42.020758+00:00',
            'email': u'ken@yahoo.com',
            'name': u'Ken'
        },
        {
            # 'created_at': '2019-03-12T16:22:22.020758+00:00',
            'email': u'joker@gmail.com',
            'name': u'joker'
        }
    ]

    schema = UserSchemaN02()  # 注意不能传 created_at 字段，因为 @post_load => return User(**data) 这个 __init__(), 无需 created_at。
    result = schema.load(user_data_s, many=True)
    data, errors = result
    pprint(data)  # [<User(name=u'Ken')>, <User(name=u'joker')>]

    # loads many 也一样（略）
