# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()  # 表的基类

# engine = create_engine('sqlite:///:memory:', echo=True)  # 连接内存数据库
engine = create_engine('postgresql://:@127.0.0.1:5432/learn')

# Base.metadata.create_all(engine)  # 使用引擎来构建我们的表

Session = sessionmaker(bind=engine)  # 创建了一个会话类
db = Session()
