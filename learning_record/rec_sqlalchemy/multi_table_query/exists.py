# -*- coding: utf-8 -*-

"""4. EXISTS 关键字

EXISTS 关键字可以在某些场景替代 JOIN 的使用。
"""

from sqlalchemy.sql import exists
from learning_record.rec_sqlalchemy.base import db
from learning_record.rec_sqlalchemy.models import Address, User

stmt = exists().where(Address.user_id == User.id)

for name, in db.query(User.name).filter(stmt):
    print(name)  # => jack

# 使用 any() 方法也能得到同样的效果：
for name, in db.query(User.name).filter(User.addresses.any()):
    print(name)

# 使用 any() 方法时也可加上查询条件：
for name, in db.query(User.name).filter(User.addresses.any(Address.email_address.like('%google%'))):
    print(name)

# 使用 has() 方法也能起到 JOIN 的作用：
db.query(Address).filter(~Address.user.has(User.name == 'jack')).all()  # 注意：这里的 ~ 符号是 “不” 的意思。


# 关系运算符
# 1. 等于、不等于
query = db.query(Address)
jack = db.query(User).filter(User.name == 'jack').one()

# 筛选 user 为 jack 的邮箱
db.query.filter(Address.user == jack)

# 筛选 user 不为 jack 的邮箱
db.query.filter(Address.user != jack)

# 2. 为空、不为空
# 筛选 user 为空的邮箱
db.query.filter(Address.user is None)

# 筛选 user 不为空的邮箱
db.query.filter(Address.user is not None)

# 3. 包含
q = db.query(User)
address = db.query(Address).filter(Address.id == 1).one()

# 筛选包含某地址的用户
query.filter(User.addresses.contains(address))
