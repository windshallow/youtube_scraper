# -*- coding: utf-8 -*-
import urlparse
from urllib import urlencode


def clean_url_param(url):
    """
    function:   清理 url 参数

    example:
    >>> url = u'https://www.youtube.com/results?sp=CAI=&search_query=beach+tent+review'
    >>>
    >>> clean_url_param(url)
    (u'https://www.youtube.com/results', {u'search_query': u'beach tent review', u'sp': u'CAI='})
    >>>
    >>> type(clean_url_param(url))
    <type 'tuple'>
    >>>

    :param url:  <type 'unicode'>, <type 'str'>   【 推荐统一使用 unicode 】
    :return:  <type 'tuple'>
    """

    result = urlparse.urlparse(url)
    param_dict = dict(urlparse.parse_qsl(result.query))         # 提取url中的参数，以字典的形式
    _url = result.scheme + u'://' + result.netloc + result.path
    return _url, param_dict


def update_url_param(url, param_dict):
    """
    function:   更新 url 参数 【 有则更新，无则创建 】

    example:
    >>> url = u'https://www.youtube.com/results?sp=CAI=&search_query=beach+tent+review'
    >>>
    >>> param_dict = {u'aaa': 111, u'bbb': 222, u'sp': u'CHANGE'}
    >>>
    >>> update_url_param(url, param_dict)
    u'https://www.youtube.com/results?search_query=beach+tent+review&sp=CHANGE&aaa=111&bbb=222'
    >>>

    :param url:   <type 'unicode'>
    :param param_dict:   <type 'dict'>
    :return:   <type 'unicode'>
    """

    result = urlparse.urlparse(url)
    _url = result.scheme + u'://' + result.netloc + result.path
    new_param_dict = dict(urlparse.parse_qsl(result.query))
    new_param_dict.update(param_dict)
    new_url = _url + u'?' + urlencode(new_param_dict)
    return new_url
