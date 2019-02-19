# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import datetime
import json
import re
import scrapy
from urllib import quote
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


class InsSpider(scrapy.Spider):

    """爬取 Instagram 关键字搜索的个人信息

    proxychains4 scrapy crawl ins_spider -a keyword=football -o ins.csv
    """

    name = "ins_spider"
    allowed_domains = ["instagram.com"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 100,
            'scrapy_spider.middlewares.CustomRetryMiddleware': 1000,
            'scrapy_spider.middlewares.RotateUserAgentMiddleware': 543,
        },

        'FEED_EXPORT_FIELDS': [
            'username', 'full_name', 'followers', 'following', 'posts', 'external_url', 'last_online', 'profile_url',
            'get_time'
        ]
    }

    def __init__(self, *args, **kwargs):
        super(InsSpider, self).__init__(*args, **kwargs)
        self.token = kwargs.get("token", "")
        self.keyword = kwargs.get("keyword", "")
        self.max_loading_times = int(kwargs.get("times", 10))
        self.loading_times = 0

    def start_requests(self):
        """
        https://www.instagram.com/web/search/topsearch/?context=blended&query=football&rank_token=0.6059456550198723&include_reel=true
        """

        url = 'https://www.instagram.com/explore/tags/%s/' % self.keyword
        if self.token:
            url = 'https://api.proxycrawl.com/?token=%s&%s&url=' % (self.token, 'country=US') + quote(url)

        yield scrapy.Request(url)

    def parse(self, response):

        target = response.text.split('<script type="text/javascript">window._sharedData =')[1].split(';</script>')[0]
        target_dict = json.loads(target)

        # print target_dict.keys()
        # csrf_token = target_dict['config']['csrf_token']

        hashtag = target_dict['entry_data']['TagPage'][0]['graphql']['hashtag']
        # print hashtag.keys()

        # id_ = hashtag['id']

        for obj_ in hashtag['edge_hashtag_to_media']['edges']:
            obj = obj_['node']
            print obj.keys()

            # display_url = obj['display_url']  # 视频主图
            # owner_id = obj['owner']['id']  # 视频发布者的id
            # taken_at_timestamp = obj['taken_at_timestamp']  # 视频发布时间戳
            shortcode = obj['shortcode']  # 可构造视频详情页url
            # video_id = obj['id']  # 猜测是视频的id

            if shortcode:
                video_url = "https://www.instagram.com/p/%s/" % shortcode
                yield scrapy.Request(video_url, callback=self.parse_video_detail, meta={})

        # 动态加载

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6",
            "Cookie": 'rur=FRC; mid=XGYzZAAEAAE4S_MNDivha2fkaI7s; csrftoken=FLhU21raeQ6QDehYPW6OwER9YmVKWLlp; '
                      'ds_user_id=11168392113; sessionid=11168392113%3A51cZNjbvVfyt1p%3A10; '
                      'urlgen="{\"95.169.14.232\": 25820}:1gvw2z:zyzt7q4eARVSpiK658AJ5dMGEqU',

            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://www.instagram.com/explore/tags/%s/" % self.keyword,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            "x-ig-app-id": "936619743392459",
            "x-instagram-gis": "b851cc79a4fcbd0e84dc0180863396b3",
            "x-requested-with": "XMLHttpRequest",
        }

        # todo 加载次数限定
        page_info = hashtag['edge_hashtag_to_media']['page_info']
        end_cursor = page_info['end_cursor']
        if page_info['has_next_page'] and self.loading_times < self.max_loading_times:
            self.loading_times += 1
            print '\n开始第%s次加载\n' % self.loading_times

            table = {
                "tag_name": self.keyword,
                "show_ranked": False,
                "first": 12,
                "after": end_cursor
            }

            query_string_parameters = json.dumps(table)

            next_url = 'https://www.instagram.com/graphql/query/?query_hash=f92f56d47dc7a55b606908374b43a314&variables=' \
                       + quote(query_string_parameters)
            yield scrapy.Request(next_url, callback=self.parse, headers=headers)
        else:
            print '加载完成 --- 加载次数: ', self.loading_times

    def parse_video_detail(self, response):

        target = response.text.split('<script type="text/javascript">window._sharedData =')[1].split(';</script>')[0]
        target_dict = json.loads(target)
        # print target_dict.keys()

        target_dict = target_dict['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        # print target_dict.keys()

        username = target_dict['owner']['username']
        profile_url = "https://www.instagram.com/" + username + "/"
        yield scrapy.Request(profile_url, callback=self.parse_profile,
                             meta={
                                 'username': username,
                                 'full_name': target_dict['owner']['full_name'],
                                 'video_url': response.url
                             })

    def parse_profile(self, response):

        item = InstagramItem()
        meta = response.meta

        item["username"] = meta.get("username")
        item["full_name"] = meta.get("full_name")

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
