# -*- coding: utf-8 -*-

"""Two-way Nesting（双向嵌套, 多对多）

1) 如果有两个对象需要相互包含, 可以指定Nested对象的  类名字符串  ,而不需要类。这样你可以包含一个  还未定义的 对象.


举个例子，Author类包含很多books，而Book对Author也有多对一的关系。



"""
from marshmallow import Schema, fields, pprint


class Author(object):
    def __init__(self, name, books=None):
        self.id = 13
        self.name = name
        self.books = [] if not books else books


class Book(object):
    def __init__(self, title, author):
        self.id = 0
        self.title = title
        self.author = author


class AuthorSchema(Schema):
    # Make sure to use the 'only' or 'exclude' params to avoid infinite recursion. (一定要使用这两个参数之一，来避免无限递归。)
    books = fields.Nested('BookSchema', many=True, exclude=('author', ))  # 外键字段，关联到不含 author 属性的 Book 对象

    class Meta:
        fields = ('id', 'name', 'books')  # Author 对象含有的字段


class BookSchema(Schema):
    author = fields.Nested(AuthorSchema, only=('id', 'name'))  # 外键字段，关联到仅含 id, name 属性的 Author 对象

    class Meta:
        fields = ('id', 'title', 'author')  # Book 对象含有的字段


if __name__ == "__main__":

    author_1 = Author(name='William Faulkner')
    book_1 = Book(title='As I Lay Dying', author=author_1)
    book_1_result, book_1_errors = BookSchema().dump(book_1)
    pprint(book_1_result, indent=2)
    # { u'author': { u'id': 13, u'name': u'William Faulkner'},
    #   u'id': 0,
    #   u'title': u'As I Lay Dying'}

    print '\n-----------------------------------\n'

    author_1.books.append(book_1)
    author_1_result, author_1_errors = AuthorSchema().dump(author_1)
    pprint(author_1_result, indent=2)
    # {
    #   "id": 13,
    #   "name": "William Faulkner",
    #   "books": [
    #     {
    #       "id": 0,
    #       "title": "As I Lay Dying"
    #     }
    #   ]
    # }
