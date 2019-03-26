# -*- coding: utf-8 -*-

"""
参考: https://segmentfault.com/a/1190000006949536

SQLAlchemy quick start

"""

db_url = '%(dialect_driver)s://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s' % {
    'dialect_driver': 'postgresql+psycopg2',
    'username': 'admin',
    'password': '',
    'host': 'localhost',
    'port': '5432',
    'database': 'admin'
}


# # ----------------------------------------------------------------------------------------
# # 6. 多表查询
# # 多表查询通常使用join进行表连接，第一个参数为表名，第二个参数为条件，例如：
#
# users = session.query(User).join(Role, Role.id == User.role_id)
#
# for u in users:
#     print u.name
#
# # join为内连接，还有左连接outerjoin，用法与join类似，右连接和全外链接在1.0版本上不支持，通常来说有这两个结合查询的方法基本够用了，1.1版本貌似添加了右连接和全外连接的支持，但是目前只是预览版
#
#
# # 还可以直接查询多个表，如下：
#
# result = session.query(User, Role).filter(User.role_id == Role.id)  # 返回用户对象及其关联的第一角色对象
# # 这里选择的是两个表，使用元组获取数据
# for u, r in result:
#     print u.name
#     print r.name
