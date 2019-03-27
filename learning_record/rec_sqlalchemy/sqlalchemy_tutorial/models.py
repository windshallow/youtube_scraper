# -*- coding: utf-8 -*-
"""
    这里的 模型类 对应数据库中的 表 。

    1）更多 字段类型 参见：
        https://docs.sqlalchemy.org/en/latest/core/type_basics.html?highlight=column%20type#generic-types

    2）Column构造函数相关设置

        必选参数：
            name： 名称，参数一，'id'           --->  不填则与字段名一致
            type_：列类型，参数二，Integer

        可选参数：
            autoincrement：自增
            default：默认值
            index：索引
            nullable：可空
            primary_key：外键

        更多介绍参见：
            https://docs.sqlalchemy.org/en/latest/core/metadata.html?highlight=column%20autoincrement#sqlalchemy.schema.Column.__init__
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()  # sqlalchemy 的  所有模型类  继承自一个由 declarative_base() 方法生成的类。


# class User(Base):
#     """用户表"""
#
#     __tablename__ = 'User'
#     id = Column('id', Integer, primary_key=True, autoincrement=True)
#     name = Column('name', String(50))
#     age = Column(Integer)  # age = Column('age', Integer) 效果一样
#
#
# class Role(Base):
#     """角色表"""
#
#     __tablename__ = 'Role'
#     id = Column('id', Integer, primary_key=True, autoincrement=True)
#     name = Column('name', String(50))
