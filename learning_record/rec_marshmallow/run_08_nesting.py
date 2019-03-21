# -*- coding: utf-8 -*-

"""Nesting Schemas（嵌套模式）

1）当模型含有外键，那这个外键的对象在Schemas如何定义。


2）Specifying Deserialization Keys（ Schema 的 field 名称定义成一样，但反序列化成不同的名字 ）
Schemas默认会 反序列化 传入字典和输出字典中相同的字段名。
如果你觉得数据不匹配你的schema，你可以传入 load_from 参数指定需要增加load的字段名（原字段名也能load，且 优先load原字段名）：


3）Specifying Serialization Keys（ Schema 的 field 名称定义成一样，但反序列化成不同的名字 ）
如果你需要序列化一个 field 成一个不同的名字时，可以使用 dump_to，逻辑和 load_from 类似。




如果field 是多个对象的集合，定义时可以使用many参数:
collaborators = fields.Nested(UserSchema, many=True)

如果外键对象是自引用，则Nested里第一个参数为'self'






"""
from marshmallow import Schema, fields, pprint
import datetime as dt


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.friends = []
        self.employer = None


class Blog(object):
    def __init__(self, title, author):
        self.title = title
        self.author = author  # A User object


# Use a Nested field to represent the relationship, passing in a nested schema class.
class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()


class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema)  # 使用 Nested field 表示外键对象：


if __name__ == "__main__":

    print '\n1）---------------- 序列化：嵌套 ----------------\n'

    user = User(name="Monty", email="monty@python.org")
    blog = Blog(title="Something Completely Different", author=user)
    result, errors = BlogSchema().dump(blog)
    pprint(result)
    # {u'author': {u'created_at': '2019-03-21T11:54:40.049316+00:00',
    #              u'email': u'monty@python.org',
    #              u'name': u'Monty'},
    #  u'title': u'Something Completely Different'}

    print '\n2）---------------- 反序列化：嵌套 ----------------\n'

    data = {
        u'author': {
            u'created_at': u'2019-03-21T11:54:40.049316+00:00',
            u'email': u'monty@python.org',
            u'name': u'Monty'
        },
        u'title': u'Something Completely Different'
    }
    result_2, errors_2 = BlogSchema().load(data)
    pprint(result_2)
    # {'author': {'created_at': datetime.datetime(2019, 3, 21, 11, 54, 40, 49316, tzinfo=tzutc()),
    #             'email': u'monty@python.org',
    #             'name': u'Monty'},
    #  'title': u'Something Completely Different'}
