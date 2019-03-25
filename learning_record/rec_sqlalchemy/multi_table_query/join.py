# -*- coding: utf-8 -*-

"""1. join 查询

假设这样一个业务场景，知道一个邮箱地址，要查询这个地址所属的用户。

# 1.1）第一个办法是用连接多个 filter() 来查询。
for u, a in session.query(User, Address).\
    filter(User.id==Address.user_id).\
    filter(Address.email_address=='jack@google.com').\
    all():

    print(u)  # => jack
    print(a)  # => jack@google.com

--------------------------------------------------------------------------------

# 1.2）更简便的方法是使用 join() 方法：
u =  session.query(User).join(Address).\
    filter(Address.email_address=='jack@google.com').\
    one()

print(u)  # => jack

# Query.join() 知道如何在 User 和 Address 之间进行连接，因为我们设定了 - 外键。

"""

from learning_record.rec_sqlalchemy.base import db


# 1.3）假如我们没有指定外键，比如这样：
from learning_record.rec_sqlalchemy.models import User, Address

# 我们可以用下面方法来让 join 生效：
# query.join(Address, User.id==Address.user_id)    # explicit condition 显式条件
# query.join(User.addresses)                       # specify relationship from left to right 指定从左到右的关系
# query.join(Address, User.addresses)              # same, with explicit target 同样,有明确的目标
# query.join('addresses')                          # same, using a string 同样,使用一个字符串

# 例子：
db.query(User).\
    join(Address, User.id == Address.user_id).\
    filter(Address.email_address == 'jack@google.com').all()
