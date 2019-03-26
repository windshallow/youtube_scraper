# -*- coding: utf-8 -*-

"""connection
    使用传统的connection的方式连接和操作数据库;
    与python自带的sqlite不同，这里不需要Cursor光标，执行sql语句不需要commit.
"""

from sqlalchemy import create_engine


# 数据库连接字符串
DB_CONNECT_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}".format(
    drivername="postgresql+psycopg2",  # default: postgresql	# psycopg2: postgresql+psycopg2
    user="admin",
    passwd="",
    host="localhost",
    port="5432",
    db_name="admin",
)

# 创建数据库引擎,echo为True,会打印所有的sql语句
engine = create_engine(DB_CONNECT_STRING, echo=True)

# 创建一个connection，这里的使用方式与python自带的sqlite的使用方式类似
with engine.connect() as con:
    # 执行sql语句，如果是增删改，则直接生效，不需要commit
    sql_statement = """SELECT * FROM quote_table WHERE id = 1;"""
    rs = con.execute(sql_statement)
    data = rs.fetchone()  # fetchone 仅匹配第一条符合
    print "Data: %s" % data
