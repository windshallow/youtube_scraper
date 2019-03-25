# -*- coding: utf-8 -*-

"""2. 子查询（subquery）- 可理解为生成新的表

情景: 需要查询每个用户所拥有的邮箱地址数量。

思路: 先对 addresses 表按用户 ID 分组，统计各组数量，这样我们得到一张新表；
     然后用 JOIN 连接新表和 users 两个表，在这里，我们应该使用 LEFT OUTER JOIN，因为使用 INTER JOIN 所得出的新表只包含两表的交集。
     (JOIN 默认为 INTER JOIN)

"""
from sqlalchemy.sql import func
from learning_record.rec_sqlalchemy.models import User, Address
from learning_record.rec_sqlalchemy.base import db


stmt_01 = db.query(Address.user_id, func.count('*').label('address_count')).\
            group_by(Address.user_id).subquery()

q_1 = db.query(User, stmt_01.c.address_count).\
        outerjoin(stmt_01, User.id == stmt_01.c.user_id).order_by(User.id).all()

for u, count in q_1:
    print(u, count)

# 执行结果
# ed None
# wendy None
# mary None
# fred None
# jack 2


# 1) 如果上面的暂时看不懂，我们先来看看第一个 stmt_01 的情况。
stmt_02 = db.query(Address.user_id, func.count('*').label('address_count')).\
    group_by(Address.user_id).all()  # 这里用了 all() 而不是 subquery()

for i in stmt_02:
    print(i)  # => (5, 2)

# 可以理解成 group_by() 方法生成了一张新的 表（ 用 subquery() 时 ）。
# 该表有两列：第一列是 user_id ，
#           第二列是该 user_id 所拥有的 addresses 的数量，这个值由 func() 跟着的方法产生，我们可以使用 c() 方法来访问这个值（即：stmt.c.address_count）。


# 2) 如果不用 outerjoin() 而使用 join()，就等于使用 SQL 中的 INTER JOIN，所得出的表只为两者交集，不会包含 None 值的列。
for i in db.query(User, stmt_01.c.address_count).\
        join(stmt_01, User.id == stmt_01.c.user_id).order_by(User.id).all():
    print(i)  # => (jack, 2)
