# -*- coding: utf-8 -*-

"""多表关系

上面的所有操作都是基于单个表的操作，下面是多表以及关系的使用，我们修改上面两个表，添加外键关联（一对多和多对一）
"""






from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.S03_session import db, engine
from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.models import Base


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))
    age = Column('age', Integer)

    # 添加角色id外键(关联到Role表的id属性)
    role_id = Column('role_id', Integer, ForeignKey('roles.id'))
    # 添加同表外键(一个用户可以有多个角色)
    second_role_id = Column('second_role_id', Integer, ForeignKey('roles.id'))

    # 添加关系属性，关联到User表(本表)的role_id外键上 - - - role就不是表里的字段了，而是属性
    role = relationship('Role', foreign_keys='User.role_id', backref='User_role_id')
    # 添加关系属性，关联到second_role_id外键上
    second_role = relationship('Role', foreign_keys='User.second_role_id', backref='User_second_role_id')


# Role模型
class Role(Base):
    __tablename__ = 'roles'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))

    # 添加关系属性，关联到User.role_id属性上(别表)
    users = relationship("User", foreign_keys='User.role_id', backref="Role_users")
    # 添加关系属性，关联到User.second_role_id属性上
    second_users = relationship("User", foreign_keys='User.second_role_id', backref="Role_second_users")


# 这里有一点需要注意的是，设置外键的时候ForeignKey('roles.id')这里面使用的是表名和表列，
# 在设置关联属性的时候relationship('Role', foreign_keys='User.role_id', backref='User_role_id')，这里的foreign_keys使用的时候类名和属性名


# 接下来就可以使用了

u = User(name='tobi', age=200)
r1 = Role(name='admin')
r2 = Role(name='user')

u.role = r1  # 用户的第一身份为r1
u.second_role = r2  # 用户的第一身份为r2

db.add(u)  # 与之关联的对象也会自动被一起add
db.commit()

# 查询（对于外键关联的关系属性可以直接访问，在需要用到的时候session会到数据库查询）
roles = db.query(Role).all()
for role in roles:  # 每个角色
    print 'role:{0} users'
    for user in role.users:  # 有哪些用户将这个角色作为第一角色
        print '\t{0}'.format(user.name)

    print 'role:{0} second_users'
    for user in role.second_users:  # 有哪些用户将这个角色作为第二角色
        print '\t{0}'.format(user.name)

# **********************
users = db.query(User).all()
for user in users:  # 每一个用户对象
    print user.role_id  # 关联的第一角色的id
    print user.second_role_id  # 关联的第二角色的id
    print user.role  # 关联的第一角色对象，一个Role类的实例对象
    print user.second_role  # 关联的第二角色对象，一个Role类的实例对象
    print user.Role_users
    print user.Role_second_users
    assert user.role == user.Role_users
    assert user.second_role == user.Role_second_users
    print dir(user)  # 返回object所有有效的属性列表

# **********************
roles = db.query(Role).all()
for role in roles:  # 每一个角色对象
    print role.users  # 以该角色为第一角色的用户对象所组成的列表
    print role.second_users  # 以该角色为第二角色的用户对象所组成的列表
    print role.User_role_id
    print role.User_second_role_id
    assert role.users == role.User_role_id
    assert role.second_users == role.User_second_role_id


# 上面表示的是一对多（多对一）的关系，还有一对一，多对多，如果要表示一对一的关系，在定义relationship的时候设置uselist为False（默认为True），如在Role中

class Role(Base):
    # ...
    user = relationship("User", uselist=False, foreign_keys='User.role_id', backref="Role_user")

