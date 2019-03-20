# -*- coding: utf-8 -*-

"""Deserializing（反序列化）

1）反序列化的方法:
    load()  方法实现 dict -> dict ,
    loads() 方法实现 json -> dict .

    load() 将 dict 等类型转换成应用层的数据结构，即orm对象：


2）dict -> object 的实现:
    首先在 schema 中自定义一个方法来实现: 传入参数 data, 返回 obj;
    然后在该方法前面加上一个 @post_load 即可 ( 使得传入的 data 即为 load 方法处理后的返回值 dict )。


3）tips:
    3.1) 对于 post_load 之类 (pre_load，post_load，pre_dump 和 post_dump) 的 事件钩子, 可以做很多拓展事情。
    3.2) @post_load 对于 load(), loads() 均有效; 猜测 其他的装饰器 也一样。

    3.3）每次调用 load(), loads() 方法之后, 会将返回值带入到  被post_load装饰  的函数的逻辑中; 。。。。。。

"""
import json
from pprint import pprint
from learning_record.rec_marshmallow.schemas import UserSchemaN01, UserSchemaN02

if __name__ == '__main__':

    user_data = {
        'created_at': '2014-08-11T05:26:03.869245',
        'email': u'ken@yahoo.com',
        'name': u'Ken'
    }
    schema = UserSchemaN01()
    result = schema.load(user_data)
    data, errors = result

    pprint(data)
    print type(data)
    pprint(errors)
    print type(errors)
    # {'name': 'Ken',
    #  'email': 'ken@yahoo.com',
    #  'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245)}  # --------------------> 应用层的数据结构
    # <type 'dict'>
    # {}
    # <type 'dict'>

    print '\n---------------- 后处理装饰器 @post_load ----------------\n'

    user_data = {
        'name': 'Ronnie',
        'email': 'ronnie@stones.com'
    }
    schema = UserSchemaN02()
    result = schema.load(user_data)
    pprint(result.data)  # => <User(name='Ronnie')>

    print '\n---------------- @post_load 对 loads() 也有效果 ----------------\n'

    json_user_data = json.dumps(user_data)  # => <type 'str'>
    schema = UserSchemaN02()
    data_2, errors = schema.loads(json_user_data)

    pprint(data_2)      # => <User(name=u'Ronnie')>
    print type(data_2)  # => <class 'learning_record.rec_marshmallow.models.User'>
    pprint(errors)      # => {}
    print type(errors)  # => <type 'dict'>
