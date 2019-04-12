# -*- coding: utf-8 -*-

import traceback
import dj_database_url
import psycopg2

from twisted.internet import defer
from twisted.enterprise import adbapi
from scrapy.exceptions import NotConfigured


class PostgreSQLWriterPipeline(object):
    """
    A spider that writes to PostgreSQL databases


    用 pipeline 把数据写入 PostgreSQL 数据库.
    注意!!! 这可不是一个好的办法，因为数据量大的时候，数据库会爆，推荐直接把 item 丢到队列里。
    这里蛮介绍一下用 pipeline 把数据写入 PostgreSQL 数据库，用于数据量小的情况下。!!!

    参考: https://www.jianshu.com/p/e0287e773d28
    """

    def open_spider(self, spider):
        """先手动创建表

        CREATE TABLE quotes_table_save_by_pipeline (
        ID SERIAL PRIMARY KEY   NOT NULL,
        author text   NOT NULL,
        quote text   NOT NULL
        );
        """
        print('爬虫开启时调用', self, dir(spider))

    @classmethod
    def from_crawler(cls, crawler):
        """Retrieves scrapy crawler and accesses pipeline's settings

        from_crawler 类方法的作用:
            https://stackoverflow.com/questions/14075941/how-to-access-scrapy-settings-from-item-pipeline
        """

        postgresql_url = crawler.settings.get('POSTGRESQL_PIPELINE_URL', None)
        if not postgresql_url:
            raise NotConfigured  # If doesn't exist, disable the pipeline

        return cls(postgresql_url)  # 创建该类的实例

    def __init__(self, postgresql_url):
        """Opens a PostgreSQL connection pool"""

        self.postgresql_url = postgresql_url
        self.report_connection_error = True  # 只报告连接错误一次

        conn_kwargs = PostgreSQLWriterPipeline.parse_postgresql_url(postgresql_url)
        self.db_pool = adbapi.ConnectionPool('psycopg2', connect_timeout=5, **conn_kwargs)  # 创建了一个数据库连接池
        # charset='utf8', use_unicode=True,

    def close_spider(self, spider):
        """Discard the database pool on spider close
            事件钩子: 所有爬虫结束后的自定义逻辑可以写在这里.
        """
        self.db_pool.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """Processes the item. Does insert into PostgreSQL"""

        logger = spider.logger

        try:
            yield self.db_pool.runInteraction(self.do_insert, item)  # 一条一条的插入，效率太低。
        except psycopg2.OperationalError:
            if self.report_connection_error:
                logger.error("Can't connect to PostgreSQL: %s" % self.postgresql_url)
                self.report_connection_error = False
        except:
            print(traceback.format_exc())

        # Return the item for the next stage. 将item返回给接下来的 pipeline 使用。
        defer.returnValue(item)

    @staticmethod
    def do_insert(tx, item):
        """Does the actual INSERT INTO （子类可覆写）"""

        sql = """INSERT INTO quotes_table_save_by_pipeline (author, quote) VALUES (%s,%s);"""

        args = (
            item["author"],
            item["quote"],
        )

        tx.execute(sql, args)

    @staticmethod
    def parse_postgresql_url(postgresql_url):
        """
        Parses postgresql url and prepares arguments for adbapi.ConnectionPool()
        """

        params = dj_database_url.parse(postgresql_url)

        conn_kwargs = dict()
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['user'] = params['USER']
        conn_kwargs['password'] = params['PASSWORD']
        conn_kwargs['database'] = params['NAME']
        conn_kwargs['port'] = params['PORT']

        # Remove items with empty values
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.items() if v)

        return conn_kwargs
