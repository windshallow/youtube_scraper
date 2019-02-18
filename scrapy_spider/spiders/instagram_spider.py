# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import datetime
import json
import re
import scrapy
from scrapy_spider.items import InstagramItem


class InstagramSpider(scrapy.Spider):

    """爬取 Instagram 关键字搜索的个人信息

    proxychains4 scrapy crawl instagram -a keyword=football -o instagram.csv
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
            # 'pk', 'username', 'full_name', 'is_private', 'profile_pic_url', 'profile_pic_id', 'is_verified',
            # 'has_anonymous_profile_picture', 'reel_auto_archive', 'mutual_followers_count', 'unseen_count',
            # 'profile_url', 'followers', 'following', 'posts', 'external_url', 'last_online'

            'username', 'full_name', 'followers', 'following', 'posts', 'external_url', 'last_online', 'profile_url',
            'get_time', 'pk', 'is_private', 'profile_pic_url', 'profile_pic_id', 'is_verified',
            'has_anonymous_profile_picture', 'reel_auto_archive', 'mutual_followers_count', 'unseen_count'

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

        # status = response_json.get('status')
        users = response_json.get('users')
        # places = response_json.get('places')
        # has_more = response_json.get('has_more')
        # rank_token = response_json.get('rank_token')
        # hashtags = response_json.get('hashtags')  # 与 keyword 相似的的标签的统计信息
        # clear_client_cache = response_json.get('clear_client_cache')

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

        item = InstagramItem()
        meta = response.meta

        item["pk"] = meta.get("pk")
        item["username"] = meta.get("username")
        item["full_name"] = meta.get("full_name")
        item["is_private"] = meta.get("is_private")
        item["profile_pic_url"] = meta.get("profile_pic_url")
        item["profile_pic_id"] = meta.get("profile_pic_id")
        item["is_verified"] = meta.get("is_verified")
        item["has_anonymous_profile_picture"] = meta.get("has_anonymous_profile_picture")
        # item["follower_count"] = meta.get("follower_count")
        item["reel_auto_archive"] = meta.get("reel_auto_archive")
        # item["byline"] = meta.get("byline")
        item["mutual_followers_count"] = meta.get("mutual_followers_count")
        item["unseen_count"] = meta.get("unseen_count")

        item["profile_url"] = response.url

        description = response.xpath('//meta[@property="og:description"]/@content').extract()[0].replace(',', '')
        item["followers"] = self.find_number('Followers', description)
        item["following"] = self.find_number('Following', description)
        item["posts"] = self.find_number('Posts', description)

        external_url = re.findall(r'"external_url":"(.+)","external_url_linkshimmed"', response.text)
        item["external_url"] = external_url

        # try:
        #     first_shortcode = re.findall(r'"shortcode":"(.+)","edge_media_to_comment":{"count"',
        #                                  response.text)[0].split('shortcode')[0].split('","edge_media_to_comment"')[0]
        # except IndexError:
        #     first_shortcode = None

        try:
            time_info = re.findall(r'"shortcode":"(.+)","edge_media_to_comment":{"count"', response.text)[0]
        except IndexError:
            time_info = ''

        bigger = 0
        for ts in re.findall(r'"taken_at_timestamp":(\d+),"dimensions"', time_info):
            ts = int(ts)
            if ts - bigger > 0:
                bigger = ts

        if bigger:
            dt1 = datetime.datetime.fromtimestamp(bigger)
            # dt1 = datetime.datetime.utcfromtimestamp(bigger)  # utc 时间
            # dt2 = datetime.datetime.utcnow()
            # ss = (dt2 - dt1).seconds  # 时间差
        else:
            dt1 = None

        item["last_online"] = dt1
        item["get_time"] = datetime.datetime.now()

        yield item

    #     if first_shortcode:
    #         video_url = "https://www.instagram.com/p/%s/" % first_shortcode
    #         yield scrapy.Request(video_url, callback=self.find_offline_time, meta={})
    #
    # def find_offline_time(self, response):
    #     pass

    @staticmethod
    def find_number(name, text):
        obj = 0
        try:
            number, unit = re.findall(r'(\d+\.?\d*)([m|k]?) %s' % name, text)[0]
            if unit == 'k':
                ratio = pow(10, 3)
            elif unit == 'm':
                ratio = pow(10, 6)
            else:
                ratio = 1

            obj = int(float(number) * ratio)
        except IndexError:
            pass
        return obj

