# -*- coding: utf-8 -*-

import treq
import json
import traceback

from urllib import quote
from twisted.internet import defer
from scrapy.exceptions import NotConfigured
from twisted.internet.error import ConnectError
from twisted.internet.error import ConnectingCancelledError


class EsWriterPipeline(object):
    """A pipeline that writes to Elastic Search

        注意：用 pipelines 向数据库插入 Items 不是个好方法。
        通常来讲，数据库更简单的方法以大量插入数据，我们应该使用这些方法大量批次插入数据，或抓取完毕之后进行后处理。
        但是，还是有很多人使用pipelines向数据库插入文件，相应的就要使用Twisted APIs。



        ES可以是无模式的，意味着我们可以不用配置就使用它。treq 也足以应付需要。
        如果想使用更高级的ES功能，我们应该使用 txes2 和其它 Python/Twisted ES包。

        treq: High-level Twisted HTTP Client API

        https://github.com/scalingexcellence/scrapybook/blob/master/ch09/properties/properties/pipelines/es.py
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Create a new instance and pass it ES's url"""

        # Get Elastic Search URL
        es_url = crawler.settings.get('ES_PIPELINE_URL', None)

        # If doesn't exist, disable
        if not es_url:
            raise NotConfigured

        return cls(es_url)

    def __init__(self, es_url):
        """Store url and initialize error reporting"""

        # Store the url for future reference
        self.es_url = es_url

    @defer.inlineCallbacks  # twisted 的装饰器
    def process_item(self, item, spider):  # 所有 pipeline 的标准 process_item() 方法都是这些参数。
        """
        Pipeline's main method. Uses inlineCallbacks to do asynchronous REST requests.

        """
        try:
            # 将 item 转换成 json 格式, 作为待插入 es 的数据。
            # ensure_ascii=False 可使结果压缩，并且没有跳过非ASCII字符。
            # .encode("utf-8") 然后将JSON字符串转化为JSON标准的默认编码 UTF-8。
            data = json.dumps(dict(item), ensure_ascii=False).encode("utf-8")
            yield treq.post(self.es_url, data, timeout=5)  # yield 延迟项

            # treq 为 twisted 的高级HTTP客户端API。
            # treq.post()方法: 模拟一个POST请求，将文档插入es。
            # es_url: http://localhost:9200/properties/property
            #         http://ES的IP地址:端口号/索引（数据库）/类型（表）

        finally:
            # In any case, return the dict for the next stage
            print('================ 开始 ================')
            yield defer.returnValue(item)
            # print('================ 结束 ================')
