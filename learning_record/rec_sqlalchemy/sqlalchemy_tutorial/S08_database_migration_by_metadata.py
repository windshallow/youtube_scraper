# -*- coding: utf-8 -*-

"""通过元数据升级数据库

    1. 上述是通过API升级和降级，我们也可以直接通过元数据更新数据库，也就是自动生成升级代码。先定义你的Model。

    2. migrations/env.py 配置元数据

        target_metadata = None

        改为:
            import os
            import sys
            sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../youtube_scraper/")))

            from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.models import Base
            from learning_record.rec_sqlalchemy.sqlalchemy_tutorial.S05_table_relationship import User, Role

            target_metadata = Base.metadata

        即: 能实现在 env.py 中导入 Base 和 待创建的表类。

    3. 创建数据库版本

        添加 --autogenerate 参数，就会从 Base.metadata 元数据中生成脚本 (xxx_add_user_table.py)

        $ alembic revision --autogenerate -m "add user table"

        由于我没有定义 account 模型，会被识别为删除，
        如果删除了model的列的声明，则会被识别为删除列，自动生成的版本我们也可以自己修改。

    4. 升级数据库
        $ alembic upgrade head



    5. 注意

        5.1 Base.metadata 声明的类必须以数据库中的一一对应，如果数据库中有的表，而在元数据中没有，会识别成删除表。

        5.2 revision 创建版本之前 执行 之前需要升级到的最新版本。

        5.3 配置Base之前，需要保证所有的Model都已经执行（即导入）过一次了，否则无法读取到，也就是需要把所有Model都import进来。

        5.4 数据库升级有风险，升级前最好先检查一遍 upgrade 函数，可以的话做好备份哈。
"""
