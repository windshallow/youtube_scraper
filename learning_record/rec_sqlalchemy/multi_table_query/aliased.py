# -*- coding: utf-8 -*-

"""3.使用别名（aliased）

SQLAlchemy  使用 aliased() 方法表示别名。当我们需要把同一张表连接多次的时候，常常需要用到别名。

"""
from sqlalchemy.orm import aliased

from learning_record.rec_sqlalchemy.base import db
from learning_record.rec_sqlalchemy.models import Address, User

# 把 Address 表分别设置别名
adalias1 = aliased(Address)
adalias2 = aliased(Address)

# 查询同时拥有两个名为："jack@google.com" 和 "j25@yahoo.com" 邮箱地址的用户。
for username, email1, email2 in db.query(User.name, adalias1.email_address, adalias2.email_address).\
                                    join(adalias1, User.addresses).\
                                    join(adalias2, User.addresses).\
                                    filter(adalias1.email_address == 'jack@google.com').\
                                    filter(adalias2.email_address == 'j25@yahoo.com'):

    print(username, email1, email2)  # => jack jack@google.com j25@yahoo.com


# 别名也可以在子查询里使用：
stmt = db.query(Address).\
        filter(Address.email_address != 'j25@yahoo.com').\
        subquery()  # 一张不含 Address.email_address == 'j25@yahoo.com' 的新 Address 表。

adalias = aliased(Address, stmt)

for user, address in db.query(User, adalias).join(adalias, User.addresses):
    print(user)  # => jack
    print(address)  # jack@google.com
