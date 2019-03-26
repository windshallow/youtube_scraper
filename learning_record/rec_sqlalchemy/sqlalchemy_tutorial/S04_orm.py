# -*- coding: utf-8 -*-

"""ORM

    上面简单介绍了sql的简单用法，既然是ORM框架，我们先定义两个模型类User和Role。接下来通过session进行增删改查.
"""

from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.models import User, Role, Base
from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.S03_session import db, engine


# 1. 创建表（如果表已经存在，则不会创建）
Base.metadata.create_all(engine)

# 2. 插入数据
u = User(name='tobi', age=200)
r = Role(name='user')

# 2.1 使用add，如果数据已经存在，会报错
db.add(u)
db.add(r)
db.commit()
print r.id

# 3 修改数据
# 3.1 使用merge方法，如果存在则修改，如果不存在则插入（只判断主键，不判断unique列）
r.name = 'admin'
db.merge(r)
db.commit()  # 要提交后才能在数据库中看到变化

db.merge(Role(name='admin2'))  # 不存在则插入
db.commit()

# 3.2 也可以通过这种方式修改
db.query(Role).filter(Role.id == 1).update({'name': 'admin1'})
db.query(Role).filter(Role.id == 3).update({'name': 'admin3'})  # 但是 Role.id == 3 不存在则不会插入
db.commit()

# 4. 删除数据
db.query(Role).filter(Role.id == 2).delete()

# 5. 查询数据
# 5.1 返回结果集的第二项
user = db.query(User).get(2)  # type(user) : __main__.User
name = db.query(User).get(2).name  # 返回名字，若无则引发 AttributeError

# 5.2 返回结果集中的第2-3项
users = db.query(User)[1:3]

# 5.3 查询条件
user = db.query(User).filter(User.id < 6).first()  # first() 返回第一个符合条件的User类型的实例对象。
users = db.query(User).filter(User.id < 6).all()

# 5.4 排序
users = db.query(User).order_by(User.name)  # 返回的User类型的实例对象们按照name属性来排序，组合成一个列表对象。默认升序。

# 5.5 降序（需要导入desc方法）
from sqlalchemy import desc

users = db.query(User).order_by(desc(User.name))

# 5.6 只查询部分属性
users = db.query(User.name).order_by(desc(User.name))
for user in users:
    print user.name

"""
In [121]: users.all()
Out[121]: [(u'tom'), (u'tobi'), (u'lucy'), (u'dady')]       # 自己造点数据

In [122]: users.all()[1]
Out[122]: (u'tobi')

In [123]: users.all()[1][0]
Out[123]: u'tobi'

In [124]: users.all()[1].name
Out[124]: u'tobi'

In [127]: users.all()[1].id
AttributeError: 'result' object has no attribute 'id'       # 可以理解为返回的User类型的实例对象们仅仅只含有name属性了。
"""

# 5.7 给结果集的列取别名
users = db.query(User.name.label('user_name')).all()  # label 标签，别名，为结果对象创建一个新的属性
for user in users:
    print user.user_name

# 5.8 去重查询（需要导入distinct方法）
from sqlalchemy import distinct

users = db.query(distinct(User.name).label('name')).all()

# 5.9 统计查询（需要导入func）
from sqlalchemy import func

user_count = db.query(User.name).order_by(User.name).count()
age_avg = db.query(func.avg(User.age)).first()  # 虽结果仅有一个对象，却不用all()，是因为会在结果再包一层[]。
age_sum = db.query(func.sum(User.age)).first()

# 5.10 分组查询
users = db.query(func.count(User.name).label('count'), User.age).group_by(User.age)  # 将年龄一样的归为一组，统计同年龄的人数
for user in users:
    print 'age:{0}, count:{1}'.format(user.age, user.count)

# 6.1 exists查询(不存在则为~exists())
from sqlalchemy.sql import exists

db.query(User.name).filter(~exists().where(
    User.role_id == Role.id))  # 问题：User表无role_id字段 ************************************ pay attention to it !
# SELECT name AS users_name FROM users WHERE NOT EXISTS (SELECT * FROM roles WHERE users.role_id = roles.id)

# 6.2 除了exists，any也可以表示EXISTS
db.query(Role).filter(
    Role.users.any())  # 问题：Role表无users字段 ************************************ pay attention to it !

# 7 random
from sqlalchemy.sql.functions import random

user = db.query(User).order_by(random()).first()
db.query(User).order_by(random()).first().name  # 随机从User表中获取一个User类的实例对象的名字

db.close()

# 方法参考：https://docs.sqlalchemy.org/en/latest/orm/internals.html?highlight=any#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any

