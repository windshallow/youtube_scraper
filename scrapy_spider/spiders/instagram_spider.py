# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import datetime
import json
import re
import time

import scrapy
from dateparser import parse

from scrapy_spider.items import SlickDealsItem


class InstagramSpider(scrapy.Spider):

    """爬取 slickdeals 的商品评论信息

    proxychains4 scrapy crawl slick_deals -o slickdeals.csv
    """

    name = "instagram"
    allowed_domains = ["instagram.com"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 100,
            'scrapy_spider.middlewares.CustomRetryMiddleware': 1000,
            'scrapy_spider.middlewares.RotateUserAgentMiddleware': 543,
        },

        'FEED_EXPORT_FIELDS': [
            'user_name', 'joined', 'title', 'posts', 'reputation', 'date_time', 'post_number', 'content',
            'email', 'up_vote', 'down_vote', 'profile'
        ]
    }

    def __init__(self, *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)

        self.keyword = kwargs.get("keyword", "")
        self.rank_token = kwargs.get("rank_token", "0.6059456550198723")

    def start_requests(self):
        """
        https://www.instagram.com/web/search/topsearch/?context=blended&query=football&rank_token=0.6059456550198723&include_reel=true
        """

        url = "https://www.instagram.com/web/search/topsearch/?context=blended&query=%s&rank_token=%s&include_reel=true"
        url = url % (self.keyword, self.rank_token)
        yield scrapy.Request(url)

    def parse(self, response):

        response_json = json.loads(response.text)

        status = response_json.get('status')
        users = response_json.get('users')
        places = response_json.get('places')
        has_more = response_json.get('has_more')
        rank_token = response_json.get('rank_token')
        hashtags = response_json.get('hashtags')  # 与 keyword 相似的的标签的统计信息
        clear_client_cache = response_json.get('clear_client_cache')

        for user_ in users:
            # item = SlickDealsItem()
            item = dict()

            item["position"] = user_.get("position")

            user = user_.get('user', {})

            item["pk"] = user.get("pk")
            item["username"] = user.get("username")  # 用于构造主页url
            item["full_name"] = user.get("full_name")
            item["is_private"] = user.get("is_private")
            item["profile_pic_url"] = user.get("profile_pic_url")  # 头像
            item["profile_pic_id"] = user.get("profile_pic_id")
            item["is_verified"] = user.get("is_verified")
            item["has_anonymous_profile_picture"] = user.get("has_anonymous_profile_picture")
            item["follower_count"] = user.get("follower_count")
            item["reel_auto_archive"] = user.get("reel_auto_archive")
            item["byline"] = user.get("byline")
            item["mutual_followers_count"] = user.get("mutual_followers_count")
            item["unseen_count"] = user.get("unseen_count")

            if item["username"]:
                profile_url = "https://www.instagram.com/" + item["username"] + "/"
                yield scrapy.Request(profile_url, callback=self.parse_profile, meta=item)

    def parse_profile(self, response):
        description = response.xpath('//meta[@property="og:description"]/@content').extract()[0]
        external_url = re.findall(r'"external_url":"(.+)","external_url_linkshimmed"', response.text)

        try:
            first_shortcode = re.findall(r'"shortcode":"(.+)","edge_media_to_comment":{"count"',
                                         response.text)[0].split('shortcode')[0].split('","edge_media_to_comment"')[0]
        except IndexError:
            first_shortcode = None

        aa = re.findall(r'"shortcode":"(.+)","edge_media_to_comment":{"count"', response.text)[0]
        small = time.time()
        for ts in re.findall(r'"taken_at_timestamp":(\d+),"dimensions"', aa):
            ts = int(ts)
            if small - ts > 0:
                small = ts

        dt1 = datetime.datetime.utcfromtimestamp(small)
        # dt2 = datetime.datetime.utcnow()
        dt2 = datetime.datetime.now()
        ss = (dt2 - dt1).seconds

    #     if first_shortcode:
    #         video_url = "https://www.instagram.com/p/%s/" % first_shortcode
    #         yield scrapy.Request(video_url, callback=self.find_offline_time, meta={})
    #
    # def find_offline_time(self, response):
    #     pass

    @staticmethod
    def cleaner(selector, index=None, replace_list=None):
        result = selector.extract()
        if type(index) == int:
            result = result[index]
            if type(replace_list) == list:
                for i in replace_list:
                    # assert type(i, basestring)
                    result = result.replace(i, '')
            result = result.replace('\n', '').replace('\r', '').replace(' ', '').strip()

        return result
