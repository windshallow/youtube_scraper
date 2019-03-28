# -*- coding: utf-8 -*-

"""数据库迁移 (通过API升级和降级)

0. sqlalchemy 的数据库 迁移/升级

    有两个库支持:
        1. alembic
        2. sqlalchemy-migrate【停止维护】

        alembic 实现了类似 git/svn 的版本管理的控制，我们可以通过 alembic 维护每次升级数据库的版本。

1. 安装

    $ pip install alembic

2. 初始化

    $ cd ~/Desktop/funny/youtube_scraper
    $ alembic init migrations

    2.1 alembic 会在根目录创建 migrations 目录和 alembic.ini 文件，如下:

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

    2.2 默认情况下创建的是基于单个数据库的。

3. 配置 alembic.ini 文件

    使用之前，需要配置一下数据库链接字符串，例如:

        sqlalchemy.url = sqlite:////Users/zhengxiankai/Desktop/database.db

        参见: http://alembic.zzzcomputing.com/en/latest/tutorial.html

4. 创建数据库版本

    4.1 接下来我们创建一个数据库版本，并新建两个表:

        $ alembic revision -m 'create table'

        创建一个版本（ 生成 yourproject/migrations/versions/xxx_create_table.py ），
        数据库迁移脚本 xxx_create_table.py 包含 upgrade 和 downgrade 两个方法，在这里添加一些新增表的逻辑 (如下代码)。


    4.2 迁移脚本的文件名是在 alembic.ini 文件中声明的。默认为: 版本号+名字，
        可以加上一些日期信息，否则不好排序:

            file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d_%%(minute).2d_%%(rev)s_%%(slug)s

    4.3 通常我们需要改一下生成模板 script.py.mako ，加上编码信息（如下），否则在升级脚本中如果有中文会报错。

        #!/usr/bin/python
        # -*- coding:utf-8 -*-

5. 升级数据库
    5.1 上述实现了 升级 和 降级 的方法，通过下面命令升级数据库到最新版本:

        $ alembic upgrade head

        这时候可以看到数据库多了两个表:
        alembic_version  --->  存放数据库版本
        account

    5.2 其他命令:

        # 升到最高版本
        $ alembic upgrade head

        # 降到最初版本
        $ alembic downgrade base

        # 升两级
        $ alembic upgrade +2

        # 降一级
        $ alembic downgrade -1

        # 升级到制定版本
        $ alembic upgrade e93b8d488143

        # 查看当前版本
        $ alembic current

        # 查看历史版本详情
        $ alembic history --verbose

        # 查看历史版本（-r参数）类似切片
        $ alembic history -r1975ea:ae1027
        $ alembic history -r-3:current
        $ alembic history -r1975ea:


"""

# """create table
#
# Revision ID: 4fd533a56b34
# Revises:
# Create Date: 2016-09-18 17:20:27.667100
#
# """

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fd533a56b34'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 添加表
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

    # 添加列
    # op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    # 删除表
    op.drop_table('account')

    # 删除列
    # op.drop_column('account', 'last_transaction_date')
