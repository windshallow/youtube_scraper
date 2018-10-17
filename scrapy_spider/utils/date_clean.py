# -*- coding: utf-8 -*-
import datetime
import pytz


def date_change(origin_date, month_dict):
    """
    function:   转换日期为标准日期    2018-03-08T00:00:00+00:00

    origin_date:   unicode
    month_dict:   dict
    """
    origin_date = origin_date.replace(u'on ', u'').replace(u',', u'').replace(u'.', u'').strip()
    origin_date = origin_date.replace(u'de ', u'')                                                  # ES
    origin_date = origin_date.replace(u'年', u' ').replace(u'月', u' ').replace(u'日', u' ').strip() # JP
    new_origin_date = origin_date.replace(u'/', u' ')  # 2017/08/29   JP  QA爬虫
    try:
        month = new_origin_date.split(u' ')[0]
        origin_date = new_origin_date.replace(month, month_dict.get(month))
        origin_date = datetime.datetime.strptime(origin_date, '%b %d %Y')          # 月 日 年
    except TypeError:
        try:
            month = new_origin_date.split(u' ')[1]
            origin_date = new_origin_date.replace(month, month_dict.get(month))
            origin_date = datetime.datetime.strptime(origin_date, '%d %b %Y')      # 日 月 年
        except ValueError:
            try:
                origin_date_list = new_origin_date.split(u' ')
                month = origin_date_list[1]
                origin_date_list[1] = month_dict.get(month)
                origin_date = u' '.join(origin_date_list)
                origin_date = datetime.datetime.strptime(origin_date, '%Y %b %d')  # 年 月 日
            except TypeError:
                print u'it does not match the format:  "ONLY DAY MONTH YEAR ! ! !"'
                origin_date = datetime.datetime(1111, 1, 11, 0, 0)
    origin_date = pytz.utc.localize(origin_date)
    origin_date = origin_date.isoformat()
    return origin_date
