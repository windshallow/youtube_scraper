# -*- coding: utf-8 -*-

import json
from elasticsearch import Elasticsearch
from twisted.internet import defer


class EsWriterPipeline(object):

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """
        Pipeline's main method. Uses inlineCallbacks to do asynchronous REST requests
        """
        es = Elasticsearch()

        data = json.dumps(dict(item), ensure_ascii=False).encode("utf-8")

        # doc_id = re.findall(r'sr=(\d*)-(\d*)', item["url"])[0][1]

        index = 'test'
        doc_type = 'doc'

        # 添加或更新数据,index，doc_type名称可以自定义，id可以根据需求赋值,body为json格式的数据内容
        # yield es.index(index=index_name, doc_type=doc_type_name, id=doc_id, body=data)
        yield es.index(index=index, doc_type=doc_type, body=data)

        # 或者:ignore=409忽略文档已存在异常
        # es.create(index="my_index", doc_type="test_type", id=1, ignore=409, body={"name": "python", "addr": "深圳"})