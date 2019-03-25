# -*- coding: utf-8 -*-
"""
参考: https://www.jianshu.com/p/594865f0681b

marshmallow格式化表单输入

常常会有这样的验证问题：
一个post表单，虽然有的位置规定了是int，但是用户总是尝试自己发送post数据，来模拟实际情况。所以是不能相信用户的输入的，故我们需要在views层收到数据时，对数据进行检验和转换。

"""
from flask import request
from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf, ContainsOnly


def convert_prefix_phone_code():
    pass


class UserLoginSchema(Schema):
    """用户登录表单"""

    CATEGORY_FACE = 1
    CATEGORY_CARD = 2

    username = fields.String(required=True)  # required表示这个字段必须要有，然后会先转换对应的类型，再通过validate函数验证。required, 默认为False。
    password = fields.String(required=True, validate=lambda x: len(x) > 0)

    phone = fields.Method('get_prefix_phone_code')  # 直接通过方法
    prefix_phone_code = fields.Function(convert_prefix_phone_code)  # 也可以通过函数

    val1 = fields.Integer(required=False, missing=5, allow_none=True)  # 如果没有出现在表单里，则给它默认值 5；以及允许None值, missing用于load。
    val2 = fields.Integer(required=True, validate=OneOf([5, 10, 20]))  # 值要在这个里面
    val3 = fields.Integer(required=False, default=5)  # 使用dump时，默认值是用default表示; missing 用于load.

    created_at = fields.DateTime(format='iso')  # 或者是iso格式的时间
    end_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')  # 或者是标准时间格式

    platform_ids = fields.List(fields.Integer(), required=True)  # 还可以是list
    # 对于list类型，要求只能包含哪些内容
    category_id = fields.List(fields.Integer(), required=True,
                              validate=ContainsOnly(
                                  choices=(
                                      CATEGORY_FACE, CATEGORY_CARD,
                                      # CATEGORY_IMAGE, CATEGORY_BODY,
                                      # CATEGORY_FACE_V2, CATEGORY_CARD_V2
                                  )
                              )
                              )

    # 如果是load时，则参数会是原来传进来的dict
    # 如果是dump时，则参数会是传进来的object
    def get_prefix_phone_code(self, obj):
        return convert_prefix_phone_code(obj.parent_end_user)

    @post_load
    def post_load_func(self, data):
        """这个修饰器很好用，表示格式化之后，调用这个函数"""
        data.val1 = 2333
        return data


if __name__ == "__main__":

    # 具体的调用方式
    data_ = request.get_json()
    data_, error = UserLoginSchema().load(data_)
    if not data_ or error:
        # 这里是异常的处理
        # 注意data需要判断是否为None，marshmallow认为None是合法的，实际业务应该是不合法的
        pass

    UserLoginSchema(only=('username',)).load(data_)  # 仅仅只验证一个fields
    UserLoginSchema(many=True).load(data_)  # 可直接处理list格式的，返回也是list
