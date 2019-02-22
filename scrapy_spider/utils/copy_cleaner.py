# -*- coding: utf-8 -*-
"""
Authored by: LRW

清洗来自拷贝的数据
"""


def headers_raw_from_chrome_to_dict(copy_data):

    """将网页上复制的请求头字符串解析成 python 字典

    :param copy_data:
    :return:

    >>> copy_data = '''
    ... accept: */*
    ... accept-encoding: gzip, deflate, br
    ... cache-control: no-cache
    ... '''
    >>>
    >>> headers_raw_from_chrome_to_dict(copy_data)
    {'accept-encoding': 'gzip, deflate, br', 'accept': '*/*', 'cache-control': 'no-cache'}
    >>>
    """
    headers_dict = {}
    [headers_dict.update(dict([i.split(': ', 1)])) for i in copy_data.split('\n') if i.strip()]
    return headers_dict
