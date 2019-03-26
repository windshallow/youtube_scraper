# -*- coding: utf-8 -*-

"""session 会话
    connection 是一般使用数据库的方式，sqlalchemy 还提供了另一种操作数据库的方式：通过session对象。
    session可以记录和跟踪数据的改变，在适当的时候提交，并且支持强大的ORM的功能。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.S01_connection import DB_CONNECT_STRING


engine = create_engine(DB_CONNECT_STRING, echo=True)

# 创建会话类
db_session = sessionmaker(bind=engine)

# 创建会话对象
session = db_session()  # 习惯命名为 db

# do something with session
# 上面创建了一个session对象，接下来可以操作数据库了，session也支持通过sql语句操作数据库

session.execute('select * from quote_table where id = 66')
session.execute("insert into quote_table(quote, author) values('hello world', 'lrw')")
session.execute("insert into quote_table(quote, author) values(:quote, :author)",
                {'quote': 'haha haha', 'author': 'lrw'})  # 注意参数使用dict，并在sql语句中使用:key占位

# 如果是增删改，需要commit
session.commit()

# 用完记得关闭，也可以用with
session.close()


db = session  # 习惯命名为 db
