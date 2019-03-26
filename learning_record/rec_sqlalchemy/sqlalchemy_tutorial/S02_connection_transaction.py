# -*- coding: utf-8 -*-

"""connection事务
    使用事务可以进行批量提交和回滚
"""

from sqlalchemy import create_engine
from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.S01_connection import DB_CONNECT_STRING


engine = create_engine(DB_CONNECT_STRING, echo=True)

with engine.connect() as connection:
    trans = connection.begin()
    try:
        r1 = connection.execute("select * from quote_table where 8 <= id and id <= 10")
        r2 = connection.execute("insert into quote_table(quote, author) values ('how time flies', 'LRW')")
        trans.commit()
    except Exception:
        trans.rollback()
        raise
