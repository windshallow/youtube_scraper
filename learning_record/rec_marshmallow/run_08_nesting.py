# -*- coding: utf-8 -*-

"""Nesting Schemas（嵌套模式）

1）当模型含有外键，那这个外键的对象在Schemas如何定义。


2）如果field 是多个对象的集合，定义时可以使用 many 参数:
collaborators = fields.Nested(UserSchema, many=True)


3）如果外键对象是自引用，则Nested里第一个参数为 'self'


4）Specifying Which Fields to Nest
如果你想指定外键对象序列化后只保留它的几个字段，可以使用 Only 参数;
如果需要选择外键对象的字段层次较多，可以使用  "."  操作符来指定。


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
    author = fields.Nested(UserSchema)  # 使用 Nested field 表示外键对象。
    # collaborators = fields.Nested(UserSchema, many=True)
    # same_blog = fields.Nested("self", many=True)


class BlogSchema2(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema, only=["email"])  # only 指定外键对象序列化后只保留它的几个字段


class SiteSchema(Schema):
    blog = fields.Nested(BlogSchema2)


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

    print '\n3）----------------  ----------------\n'

    schema = BlogSchema2()
    result_3, errors_3 = schema.dump(blog)
    pprint(result_3)
    # {'title': u'Something Completely Different',
    #  'author': {'email': u'monty@python.org'}}

    print '\n4）---------------- "."  操作符 ----------------\n'

    site = {'blog': data}

    schema = SiteSchema(only=['blog.author.email'])
    result_4, errors_4 = schema.dump(site)
    pprint(result_4)
    # {u'blog': {u'author': {u'email': u'monty@python.org'}}}
