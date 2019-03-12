# -*- coding: utf-8 -*-

"""Deserializing（反序列化）

反序列化使用 schema 中的 load() 或 loads() 方法，其中:
    load() 方法实现 dict -> dict，
    loads()方法实现 json -> dict，

    load() 将 dict 等类型转换成应用层的数据结构，即orm对象：


对反序列化而言，将传入的 dict 变成 object 更加有意义。
在Marshmallow中，dict -> object的方法需要自己实现，然后在该方法前面加上一个decoration：post_load 即可。

tips: 1) 对于 post_load 之类 (pre_load，post_load，pre_dump 和 post_dump) 的 事件钩子, 可以做很多拓展事情。
      2) @post_load 对于 load(), loads() 均有效; 猜测 其他的装饰器 也一样。

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
    #  'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245)}
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

    print '\n---------------- loads() ----------------\n'

    json_user_data = json.dumps(user_data)  # => <type 'str'>
    schema = UserSchemaN02()
    data_2, errors = schema.loads(json_user_data)

    pprint(data_2)      # => <User(name=u'Ronnie')>
    print type(data_2)  # => <class 'learning_record.rec_marshmallow.models.User'>
    pprint(errors)      # => {}
    print type(errors)  # => <type 'dict'>
