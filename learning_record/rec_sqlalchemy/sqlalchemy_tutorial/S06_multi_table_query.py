# -*- coding: utf-8 -*-

"""多表查询 -- 相互关联的表才可以多表查询

多表查询通常使用 join 进行表连接。

    join      为 内连接（常用）
    outerjoin 为 左连接（用法与join类似）

通常来说有这两个结合查询的方法基本够用了。

"""

from learning_record.rec_sqlalchemy.base import db
from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.S05_table_relationship import User, Role


if __name__ == "__main__":

    run_block = 1

    if run_block == 1:

        users = db.query(User).join(Role, Role.id == User.role_id)  # join(表名, 条件); query() 中的参数表示返回结果的类型（包含在[]中）
        for u in users:
            print u.name

    if run_block == 2:
        # 直接查询多个表
        result = db.query(User, Role).filter(User.role_id == Role.id)
        for u, r in result:  # 这里选择的是两个表【query(User, Role)】，使用元组获取数据
            print u.name, r.name
