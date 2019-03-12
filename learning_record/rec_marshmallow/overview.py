# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load, pprint


# ======================================================================================================================
# Two-way Nesting
# 如果有两个对象需要相互包含, 可以指定Nested对象的类名字符串, 而不需要类, 这样你可以包含一个还未定义的对象。
# ======================================================================================================================


class Author(object):
    def __init__(self, name):
        self.id = 1
        self.name = name
        self.books = []


class Book(object):
    def __init__(self, title, author):
        self.id = 0
        self.title = title
        self.author = author


class AuthorSchema(Schema):
    # Make sure to use the 'only' or 'exclude' params to avoid infinite recursion
    books = fields.Nested('BookSchema', many=True, exclude=('author', ))

    class Meta:
        fields = ('id', 'name', 'books')


class BookSchema(Schema):
    author = fields.Nested(AuthorSchema, only=('id', 'name'))

    class Meta:
        fields = ('id', 'title', 'author')


# ======================================================================================================================
# Nesting A Schema Within Itself
# 如果需要自引用(即, 引用同类型的对象), "Nested"构造时传入"self" (包含引号)即可。
# 注意避免个别字段无限递归
# ======================================================================================================================

class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()

    friends = fields.Nested('self', many=True)
    # Use the 'exclude' argument to avoid infinite recursion 避免无限递归, 自引用不能再包含 employer 字段。
    employer = fields.Nested('self', exclude=('employer', ), default=None)


if __name__ == '__main__':

    from learning_record.rec_marshmallow.models import User
    user = User("Steve", 'steve@example.com')
    user.friends.append(User("Mike", 'mike@example.com'))
    user.friends.append(User('Joe', 'joe@example.com'))
    user.employer = User('Dirk', 'dirk@example.com')
    result = UserSchema().dump(user)
    # pprint(result.data, indent=2)

    """Output
{
    "name": "Steve",
    "email": "steve@example.com",
    "friends": [
        {
            "name": "Mike",
            "email": "mike@example.com",
            "friends": [],
            "employer": null
        },
        {
            "name": "Joe",
            "email": "joe@example.com",
            "friends": [],
            "employer": null
        }
    ],
    "employer": {
        "name": "Dirk",
        "email": "dirk@example.com",
        "friends": []
    }
}
    """

    author_1 = Author(name='William Faulkner')
    book = Book(title='As I Lay Dying', author=author_1)
    book_result, errors = BookSchema().dump(book)
    # pprint(book_result, indent=2)
    # {
    #   "id": 124,
    #   "title": "As I Lay Dying",
    #   "author": {
    #     "id": 8,
    #     "name": "William Faulkner"
    #   }
    # }

    author_result, errors = AuthorSchema().dump(author_1)
    pprint(author_result, indent=2)
    # {
    #   "id": 8,
    #   "name": "William Faulkner",
    #   "books": [
    #     {
    #       "id": 124,
    #       "title": "As I Lay Dying"
    #     }
    #   ]
    # }
