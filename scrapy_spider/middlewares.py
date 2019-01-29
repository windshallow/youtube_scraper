# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import random  # 导入随机模块
import logging
import time
import scrapy

# 与爬虫更换浏览器头有关的配置
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from utils import ua_list  # 导入与robot同级的ua_list.py模块

# 与爬虫重试有关的配置
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
# from robot.exceptions import ParseError

from scrapy.utils.response import response_status_message


class ScrapySpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CustomRetryMiddleware(RetryMiddleware):           # 自定义重试中间件，就添加了个自定义的ParseError情况。详见源码

    """
    https://github.com/scrapy/scrapy/blob/master/scrapy/downloadermiddlewares/retry.py
    """

    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           # ParseError,
                           IOError)

    def _retry(self, request, reason, spider):
        super(CustomRetryMiddleware, self)._retry(request, reason, spider)


class RotateUserAgentMiddleware(UserAgentMiddleware):   # 循环用户代理中间件
    def __init__(self, user_agent=''):                  # 初始化 注意一定是 user_agent=''
        super(RotateUserAgentMiddleware, self).__init__(user_agent)
        self.user_agent = user_agent

    def process_request(self, request, spider):         # 当每个request通过下载中间件时，该方法被调用。
        ua = random.choice(self.user_agent_list)        # 随机选取一个浏览器代理
        if ua:
            # print "********Current UserAgent:%s************" % ua
            request.headers.setdefault('User-Agent', ua)

    # http://www.useragentstring.com/pages/useragentstring.php  # 从这个网站爬下来的浏览器代理
    user_agent_list = ua_list.UA_LIST                           # user_agent_list 必须是一个列表字符串对象


# class UserAgentmiddleware(UserAgentMiddleware):
#     def process_request(self, request, spider):
#         agent = random.choice(USA)
#         request.headers["User-Agent"] = agent
