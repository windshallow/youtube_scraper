# -*- coding: utf-8 -*-
"""
https://pynash.org/2013/02/15/using-sqlalchemy-func-and-group/
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label

Base = declarative_base()  # 表的基类


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    balance = Column(Float)
    group = Column(String)

    def __init__(self, name, fullname, balance, group):
            self.name = name
            self.fullname = fullname
            self.balance = balance
            self.group = group


user1 = User('Bob', 'Big Bob', 1000000.00, 'Mob')
user2 = User('Linda', 'Linda Lu', 100.50, 'Diner')
user3 = User('Lil Bob', 'Bobby Jr', 100500.00, 'Mob')
user4 = User('Rachael', 'Rachael Rach', 125.50, 'Personal')

if __name__ == '__main__':

    # engine = create_engine('sqlite:///:memory:', echo=True)  # 连接内存数据库
    engine = create_engine('postgresql://:@127.0.0.1:5432/learn')

    Base.metadata.create_all(engine)  # 使用引擎来构建我们的表

    # 现在我们有了一个Model和一个表，并且它们已连接，我们可以添加一些数据。
    Session = sessionmaker(bind=engine)  # 创建了一个会话类
    db = Session()

    db.add(user1)
    db.add(user2)
    db.add(user3)
    db.add(user4)
    db.commit()

    # 查询
    for user in db.query(User).all():
        print user.name, user.balance
        print '\n--------------------\n'

    results = db.query(User.group,
                       label('members', func.count(User.id)),  # members 为新建的标签名。
                       label('total_balance', func.sum(User.balance))  # query 中查询几个字段就返回这几个字段的结果。
                       ).group_by(User.group).all()
    # group_by(User.group) 按 group 一样的划分到同一组
    # [(u'Diner', 1, 100.5), (u'Mob', 2, 1100500.0), (u'Personal', 1, 125.5)]

    for result in results:
        print "%s has %i members with a balance of %d" % (result.group, result.members, result.total_balance)
