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

    """
    一个用户 的 第一角色 只能是 一个角色（同理第二角色）;
    一个角色可以被多个用户作为 第一角色 或者 第二角色 .

    故:
        用户是一, 角色是多;
        外键定义在 "一" 的模型上                   ==>  外键字段 返回 单个的 关联对象的关联字段。
        关系属性 relationship 定义在 "多" 的模型上  ==>  关系属性 返回 与之关联的对象所组成的 list。

        特殊情况:
            "一" 的模型也可以定义关系属性, 该属性关联到本表的外键上，直接返回关联的 对象（而不是关联字段）。
            其实这种做法有点多余:
                直接在定义 "多" 的模型上 relationship 时添加 --> backref="Role_users" 即可。

    """

    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))
    age = Column('age', Integer)

    # 外键字段
    role_id = Column('role_id', Integer, ForeignKey('roles.id'))  # 添加角色id外键(关联到Role表的id属性)
    second_role_id = Column('second_role_id', Integer, ForeignKey('roles.id'))  # 添加同表 (Role) 外键(一个用户可以有多个角色)

    # 关系属性, 不是表中的字段 (多余)
    role = relationship('Role', foreign_keys='User.role_id', backref='User_role_id')  # 关联到User表(本表)的role_id外键上
    second_role = relationship('Role', foreign_keys='User.second_role_id', backref='User_second_role_id')


class Role(Base):

    __tablename__ = 'roles'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(50))

    # 关系属性, 不是表中的字段
    users = relationship("User", foreign_keys='User.role_id', backref="Role_users")  # 关联到User.role_id属性上(别表)
    second_users = relationship("User", foreign_keys='User.second_role_id', backref="Role_second_users")

# 设置外键字段 role_id:
#   role_id = Column('role_id', Integer, ForeignKey('roles.id'))
#   其中: 'roles.id'  =>  表名.表列

# 设置关联属性 users:
#   users = relationship("User", foreign_keys='User.role_id', backref="Role_users")
#
#   users 返回与之关联的对象所组成的 list.
#
#   其中: foreign_keys='User.role_id'  =>  类名.外键名 ----- 用来找关联对象
#        backref="Role_users"  =>  为关联该 Role实例对象 的 某个User实例对象 添加一个 Role_users 属性，返回该 Role实例对象（非列表）。


if __name__ == "__main__":

    run_block = 3

    if run_block == 1:
        Base.metadata.create_all(engine)  # models 里的 同名 User，Role 表得注释掉，否则报错。

    if run_block == 2:
        u = User(name='tobi', age=200)
        r1 = Role(name='admin')
        r2 = Role(name='user')

        u.role = r1  # 用户的第一角色为r1
        u.second_role = r2  # 用户的第二角色为r2

        db.add(u)  # 与之关联的对象也会自动被一起add
        db.commit()

    if run_block == 3:
        # 查询（对于外键关联的 关系属性 可以直接访问，在需要用到的时候 session 会到数据库查询）

        roles = db.query(Role).all()  # roles: 所有角色对象组成的list
        for role in roles:
            for user in role.users:  # role.users: 以该角色作为第一角色的 用户对象组成的list
                print '\n用户: {0} ---> 第一角色: {1}\n'.format(user.name, role.name)

            for user in role.second_users:
                print '\n用户: {0} ---> 第二角色: {1}\n'.format(user.name, role.name)

        users = db.query(User).all()  # users: 所有用户对象组成的list
        for user in users:

            print user.role_id  # 关联的第一角色的id
            print user.role  # 关联的第一角色对象，一个Role类的实例对象
            print user.Role_users
            assert user.role == user.Role_users

            print user.second_role_id  # => 2
            print user.second_role  # => <__main__.Role at 0x10ecdac50>
            print user.Role_second_users
            assert user.second_role == user.Role_second_users

            print dir(user)

        roles = db.query(Role).all()
        for role in roles:
            print role.users  # => [<__main__.User at 0x10ecda550>]
            print role.User_role_id  # => [<__main__.User at 0x10ecda550>]
            assert role.users == role.User_role_id

            print role.second_users
            print role.User_second_role_id
            assert role.second_users == role.User_second_role_id
