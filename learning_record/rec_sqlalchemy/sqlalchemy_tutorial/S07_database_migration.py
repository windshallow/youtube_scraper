# -*- coding: utf-8 -*-

"""数据库迁移

sqlalchemy 的数据库 迁移/升级 有两个库支持:
    1. alembic
    2. sqlalchemy-migrate【停止维护】

alembic 实现了类似 git/svn 的版本管理的控制，我们可以通过 alembic 维护每次升级数据库的版本。



1. 安装

    $ pip install alembic
2. 初始化

    $ cd ~/Desktop/funny/youtube_scraper
    $ alembic init migrations

    alembic 会在根目录创建 migrations 目录和 alembic.ini 文件，如下:

        yourproject/
            alembic.ini     -------------------------> 提供了一些基本的配置（注意要先配置）
            migrations/
                env.py      -------------------------> 每次执行Alembic都会加载这个模块，主要提供项目Sqlalchemy Model 的连接
                README
                script.py.mako      -------------------------> 迁移脚本生成模版
                versions/           -------------------------> 存放生成的迁移脚本目录
                    3512b954651e_add_account.py
                    2b1ae634e5cd_add_order_id.py
                    3adcc9a56557_rename_username_field.py

    默认情况下创建的是基于单个数据库的。

3. 配置

    使用之前，需要配置一下链接字符串，打开 alembic.ini 文件，设置 sqlalchemy.url 连接字符串，例如:

        sqlalchemy.url = sqlite:////Users/zhengxiankai/Desktop/database.db

    其他参数可以参见官网说明：http://alembic.zzzcomputing.com/en/latest/tutorial.html

"""