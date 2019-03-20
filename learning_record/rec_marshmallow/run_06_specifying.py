# -*- coding: utf-8 -*-

"""Specifying（指定）

1）Specifying Attribute Names （ Schema 的 field 名称可以定义成不一样 ）
Schemas 默认会 序列化 传入对象 和 自身定义的fields 相同的属性。 [即：你定义的 schema 属性名称 和 你传入的对象的字段要一致，否则该属性会得不到值]
但是你可以定义这个 fields（属性名）的值 从你传入的某个字段中取（这时候 fields 就可以避免名字不同而取不到值）。


2）Specifying Deserialization Keys（ Schema 的 field 名称定义成一样，但反序列化成不同的名字 ）
Schemas默认会 反序列化 传入字典和输出字典中相同的字段名。
如果你觉得数据不匹配你的schema，你可以传入 load_from 参数指定需要增加load的字段名（原字段名也能load，且 优先load原字段名）：


3）Specifying Serialization Keys（ Schema 的 field 名称定义成一样，但反序列化成不同的名字 ）
如果你需要序列化一个 field 成一个不同的名字时，可以使用 dump_to，逻辑和 load_from 类似。

"""
from marshmallow import Schema, fields, pprint
from learning_record.rec_marshmallow.models import User

user = User('Keith', email='keith@stones.com')


if __name__ == "__main__":

    print '\n1）---------------- 序列化：attribute ----------------\n'

    class UserSchema(Schema):
        name = fields.String()

        email_addr = fields.String(attribute="email")  # email_addr 字段从 email 属性取值。
        date_created = fields.DateTime(attribute="created_at")  # date_created 字段从 created_at 属性取值。

    data_1, errors_1 = UserSchema().dump(user)
    pprint(data_1)
    # {'name': 'Keith',
    #  'email_addr': 'keith@stones.com',
    #  'date_created': '2014-08-17T14:58:57.600623+00:00'}

    print '\n\2）---------------- 反序列化：load_from ----------------\n'

    class UserSchemaN01(Schema):
        name = fields.String()
        email = fields.Email(load_from='emailAddress')

    data = {
        'name': 'Mike',
        'emailAddress': 'foo@bar.com',
        # 'email': '会比emailAddress优先load@gmail.com'  # 有同名称时，会优先load同名称的数据。
    }

    data_2, errors_2 = UserSchemaN01().load(data)
    pprint(data_2)
    # {'name': u'Mike',
    # 'email': 'foo@bar.com'}

    print '\n\2）---------------- 序列化：dump_to ----------------\n'

    class UserSchemaN02(Schema):
        name = fields.String(dump_to='TheName')
        email = fields.Email(load_from='CamelCasedEmail', dump_to='CamelCasedEmail')

    data = {
        'name': 'Mike',
        'email': 'foo@bar.com'
    }

    result, errors = UserSchemaN02().dump(data)
    pprint(result)
    # {'TheName': u'Mike',
    # 'CamelCasedEmail': 'foo@bar.com'}
