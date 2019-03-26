# -*- coding: utf-8 -*-

"""connection事务

    使用事务可以进行批量提交和回滚
"""

from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.S01_connection import engine


if __name__ == "__main__":

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            r1 = connection.execute("select * from users where 2 <= id and id <= 3")
            print r1
            r2 = connection.execute("insert into users(name, fullname, balance) values "
                                    "('lrw', 'big lrw', 666)")
            trans.commit()
        except Exception:
            trans.rollback()
            raise
