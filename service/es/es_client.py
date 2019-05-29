# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch

from scrapy_spider import settings

es = Elasticsearch(getattr(settings, 'ELASTICSEARCH_URL', None))  # 暂时


class ElasticSearchUtil(object):

    def __init__(self):
        self.conn = es

    def __del__(self):
        self.close()

    def check(self):
        """当前系统的ES信息"""

        return self.conn.info()

    def insert(self, index, doc_type, doc, doc_id=None):
        """插入一条文档到指定的索引中

        POST http://localhost:9200/index/doc_type

        :param index: 指定的索引
        :param doc_type: 文档类型
        :param doc: 文档
        :param doc_id: 可自定义文档id值, 若不指定, ES会自动生成
        :return:
        """
        return self.conn.index(index=index, doc_type=doc_type, body=doc, id=doc_id)

    def batch_insert(self, index, doc_type, batch_doc):
        """批量文档插入

        bulk接口所要求的数据列表结构为:[{{optionType}: {Condition}}, {data}]
        其中:
        optionType: 可为index、delete、update
        Condition: 可设置每条数据所对应的index值和type值
        data: 为具体要插入/更新的单条数据

        :param index: 指定的索引
        :param doc_type: 文档类型
        :param batch_doc: 批量文档
        :return:
        """

        header = [{"index": {}} for i in range(len(batch_doc))]
        temp = [dict] * (len(batch_doc) * 2)
        temp[::2] = header
        temp[1::2] = batch_doc
        try:
            return self.conn.bulk(index=index, doc_type=doc_type, body=temp)
        except Exception as e:
            return str(e)

    def search_doc_by_query(self, index=None, doc_type=None, dsl_query_body=None):
        """dsl筛选语句查询es文档

        :param index:
        :param doc_type:
        :param dsl_query_body: 筛选语句, 符合DSL语法格式

        {"query": {"match_all": {}}}
        {'query': {'range': {'suggested_bid': {'gte': 2.5, 'lte': 3}}}}  #  2.5 <= suggested_bid <=3
        {'query': {'range': {'request_date': {'lte': arrow.get(2018, 9, 28).to('Asia/Shanghai').datetime}}}}
        {'query': {'match': {'amazon_keyword_id': '94281538640783'}}}

        :return:
        """

        return self.conn.search(index=index, doc_type=doc_type, body=dsl_query_body, size=10000, from_=0)

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                pass
            finally:
                self.conn = None
