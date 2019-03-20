# -*- coding: utf-8 -*-

"""Validation（验证）

1）Schema.load() 和 loads() 方法会在 返回值 中加入验证错误的 dictionary，例如email和URL都有内建的验证器。

2）当验证一个集合 (many) 时，返回的错误dictionary会以错误序号对应错误信息的  key: value 形式保存。 其中 key 为 索引号。

3）向 内建的field 中传入 validate 参数来定制验证的逻辑。validate的值可以是函数，匿名函数lambda，或者是定义了 __call__ 的对象。

4）如果你传入的函数中定义了 ValidationError，当它触发时，错误信息会得到保存。

5）只验证数据，而不生成对象，可以使用 Schema.validate() 。

注意1：
如果你需要执行多个验证，你应该传入可调用的验证器的集合（list, tuple, generator）

注意2：
Schema.dump() 也会返回错误信息dictionary，也会包含序列化时的所有ValidationErrors。但是:
    required,                # True, 则该字段必填。
    allow_none,
    validate,
    @validates,              # 使用validates 装饰器就可以为某字段注册一个验证方法。
    @validates_schema
    均只用于反序列化，即: Schema.load()。

"""
from learning_record.rec_marshmallow.overview import UserSchema
from learning_record.rec_marshmallow.schemas import BandMemberSchema, ValidatedUserSchema, ItemSchema, ItemSchemaN01, \
    UserSchemaN03

if __name__ == "__main__":

    print '\n1）---------------- fields.Email 有内建的验证器 ----------------\n'

    data, errors = UserSchema().load({'email': 'foo'})
    print errors  # => {'email': ['"foo" is not a valid email address.']}
    # OR, equivalently
    result = UserSchema().load({'email': 'foo'})
    print result.errors  # => {'email': ['"foo" is not a valid email address.']}

    print '\n2）---------------- many ----------------\n'

    user_data = [
        {'email': 'mick@stones.com', 'name': 'Mick'},
        {'email': 'invalid', 'name': 'Invalid'},  # invalid email
        {'email': 'keith@stones.com', 'name': 'Keith'},
        {'email': 'charlie@stones.com'},  # missing "name"
    ]

    result = BandMemberSchema(many=True).load(user_data)
    print result.errors
    # {1: {'email': ['"invalid" is not a valid email address.']},
    #  3: {'name': ['Missing data for required field.']}}

    print '\n3）---------------- validate ----------------\n'

    in_data = {'name': 'Mick', 'email': 'mick@stones.com', 'age': 71}
    result = ValidatedUserSchema().load(in_data)
    print result.errors  # => {'age': [u'Invalid value.']}

    print '\n4）---------------- 定义且保存报错信息 ----------------\n'
    
    in_data = {'quantity': 31}
    result, errors = ItemSchema().load(in_data)
    print errors  # => {'quantity': ['Quantity must not be greater than 30.']}

    print '\n5）---------------- @validates ----------------\n'

    in_data = {'quantity': 31}
    result_, errors = ItemSchemaN01().load(in_data)
    print errors  # => {'quantity': ['Quantity must not be greater than 30.']}

    print '\n6）---------------- required 及 自定义报错信息 ----------------\n'

    data_6, errors = UserSchemaN03().load({'email': 'foo@bar.com'})
    print errors
    # {'name': ['Missing data for required field.'],
    #  'age': ['Age is required.'],
    #  'city': {'message': 'City required', 'code': 400}}

    print '\n7）---------------- 只验证数据，不生成对象 ----------------\n'

    errors = UserSchema().validate({'name': 'Ronnie', 'email': 'invalid-email'})
    print errors  # {'email': ['"invalid-email" is not a valid email address.']}
