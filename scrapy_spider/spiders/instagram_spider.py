# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import csv
import datetime
import hashlib
import json
import random
import re
from time import sleep, time, strftime, localtime

import scrapy
import requests
from urllib import quote, unquote
from collections import OrderedDict
from scrapy_spider.items import InstagramItem
from scrapy_spider.utils import ua_list


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
    allowed_domains = ["instagram.com", "api.proxycrawl.com"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 100,
            'scrapy_spider.middlewares.CustomRetryMiddleware': 1000,
        },

        'FEED_EXPORT_FIELDS': [
            'username', 'full_name', 'followers', 'following', 'posts', 'highlight_reel_count', 'business_phone_number',
            'business_email', 'business_category_name', 'business_address', 'is_business_account', 'is_joined_recently',
            'biography', 'external_url', 'last_online', 'profile_url', 'get_time', 'keyword'
        ]
    }

    def __init__(self, *args, **kwargs):
        super(InsSpider, self).__init__(*args, **kwargs)
        self.token = kwargs.get("token", "")
        self.keyword = kwargs.get("keyword", "")
        self.max_loading_times = int(kwargs.get("times", 10))
        self.loading_times = 0

        self.ua = random.choice(ua_list.UA_LIST)
        self.query_hash = 'f92f56d47dc7a55b606908374b43a314'

        self.container = set()

    def start_requests(self):
        """
        https://www.instagram.com/web/search/topsearch/?context=blended&query=football&rank_token=0.6059456550198723&include_reel=true
        """

        url = 'https://www.instagram.com/explore/tags/%s/' % self.keyword
        if self.token:
            url = 'https://api.proxycrawl.com/?token=%s&%s&url=' % (self.token, 'country=US') + quote(url)

        yield scrapy.Request(url)

    @staticmethod
    def cookie(csrf_token):
        """返回 cookie_string, 用于 request.headers"""

        # todo 可以考虑发起一次主页的请求来设置这些参数，更灵活一些。
        cookie = {
            'rur': 'FRC',
            'mid': 'XGYzZAAEAAE4S_MNDivha2fkaI7s',  # 不同加载请求中，该值不会更改
            'csrftoken': csrf_token,
            'ds_user_id': '11168392113',
            'sessionid': '11168392113%3A51cZNjbvVfyt1p%3A10',
            'urlgen': '"{\"95.169.14.232\": 25820}:1gwi7Q:Pbk2T58XBuljTG9wEj94ODVaddc"',
        }
        sequence = ['rur', 'mid', 'csrftoken', 'ds_user_id', 'sessionid', 'urlgen']
        cookie = ''.join([k + '=' + cookie[k] + '; ' for k in sequence])[: -2]

        return cookie

    @property
    def user_agent(self):
        """保证对于一次 explore 操作下的所有js加载的 user_agent 一致, 才能更加近似于手动操作"""

        return self.ua

        # return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
        #        'Chrome/72.0.3626.109 Safari/537.36'

    def x_instagram_gis(self, rhx_gis):

        """签名
        https://stackoverflow.com/questions/49786980/how-to-perform-unauthenticated-instagram-web-scraping-in-response-to-recent-priv

        "{rhx_gis}:{path}"
        """

        md5 = hashlib.md5()
        path = '/explore/tags/%s/' % self.keyword
        string = "{rhx_gis}:{path}".format(rhx_gis=rhx_gis, path=path)
        md5.update(string)
        x_instagram_gis = md5.hexdigest()

        return x_instagram_gis

    def headers(self, csrf_token, rhx_gis):
        """请求头
            备注: 所有加载请求的 csrf_token 均一致;
                 x_instagram_gis 均不一致, 即 rhx_gis 不一致（目前暂用一致，貌似也能跑）。
        """

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6',
            'cache-control': 'no-cache',
            'cookie': self.cookie(csrf_token),
            'pragma': 'no-cache',
            'referer': 'https://www.instagram.com/explore/tags/%s/' % self.keyword,
            'user-agent': self.user_agent,
            'x-ig-app-id': '936619743392459',  # 貌似不会变用同一台机器抓的时候
            'x-instagram-gis': self.x_instagram_gis(rhx_gis),
            'x-requested-with': 'XMLHttpRequest',
        }

        return headers

    def js_query_url(self, query_hash, end_cursor):
        """动态加载url"""

        table = OrderedDict([
            ("tag_name", self.keyword),
            ("show_ranked", False),
            ("first", random.randint(3, 20)),
            ("after", end_cursor)
        ])
        query_string_parameters = quote(json.dumps(table, sort_keys=False).replace(' ', ''))  # key有排序

        url = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={variables}'.format(
            query_hash=query_hash, variables=query_string_parameters
        )
        return url

    def parse(self, response):
        """第一次解析 explore 页面（非js）"""

        target = response.text.split('<script type="text/javascript">window._sharedData =')[1].split(';</script>')[0]
        target_dict = json.loads(target)  # dict

        csrf_token = target_dict['config']['csrf_token']
        rhx_gis = target_dict['rhx_gis']

        hashtag = target_dict['entry_data']['TagPage'][0]['graphql']['hashtag']  # dict
        # id_ = hashtag['id']

        for obj_ in hashtag['edge_hashtag_to_media']['edges']:
            obj = obj_['node']  # print obj.keys()

            # display_url = obj['display_url']  # 视频主图
            # owner_id = obj['owner']['id']  # 视频发布者的id
            # taken_at_timestamp = obj['taken_at_timestamp']  # 视频发布时间戳
            # video_id = obj['id']  # 猜测是视频的id

            shortcode = obj['shortcode']  # 可构造视频详情页url
            self.container.add(shortcode)

            # 2019.2.27 单独拆开 ** ----------- **** ----------- **** ----------- **** ----------- **
            if shortcode:
                video_url = "https://www.instagram.com/p/%s/" % shortcode
                yield scrapy.Request(video_url, callback=self.parse_video_detail, meta={})

        # 动态加载
        page_info = hashtag['edge_hashtag_to_media']['page_info']
        end_cursor = page_info['end_cursor']
        if page_info['has_next_page'] and self.loading_times < self.max_loading_times:
            self.loading_times += 1
            print '\n开始第%s次加载\n' % self.loading_times

            js_query_url = self.js_query_url(self.query_hash, end_cursor)
            # import ipdb;ipdb.set_trace()

            # 神奇的是scrapy.Request 居然不可以，而 Requests 模块居然可以。
            # yield scrapy.Request(js_query_url, callback=self.parse_js_response,
            #                      headers=self.headers(csrf_token, rhx_gis),
            #                      meta={'csrf_token': csrf_token})

            result = self.parse_js_requests(js_query_url, csrf_token, rhx_gis)
            if result['has_next_page']:
                yield scrapy.Request(self.transition_url(), callback=self.parse_transition_url, meta=result,
                                     dont_filter=True)

        else:
            print '加载完成 --- 加载次数: ', self.loading_times

    def parse_js_requests(self, js_query_url, csrf_token, rhx_gis):
        """伪parse: 解析js请求"""

        sleep(random.uniform(1, 5))  # 模拟人的操作
        response = requests.get(js_query_url, headers=self.headers(csrf_token, rhx_gis))

        target_dict = json.loads(response.text)
        short = target_dict['data']['hashtag']
        media = short['edge_hashtag_to_media']

        sum_count = len(media['edges'])
        self.loading_times += 1
        print '第 %s 次加载的视频个数: %s' % (self.loading_times, sum_count)

        short_codes = set()
        for i in media['edges']:
            short_codes.add(i['node']['shortcode'])
            self.container.add(i['node']['shortcode'])

        # ----------------------------------------- 每段做一次保存
        if len(self.container) >= 2000:
            self.save_shortcode()
            self.container = set()

        end_cursor = media['page_info']['end_cursor']
        has_next_page = media['page_info']['has_next_page']

        return {
            'shortcode': list(short_codes),
            'has_next_page': has_next_page,

            # 构造下一次js请求的参数
            'js_query_url': self.js_query_url(query_hash=self.query_hash, end_cursor=end_cursor),
            'csrf_token': csrf_token,
            'rhx_gis': rhx_gis
        }

    def parse_transition_url(self, response):
        """作为过渡解析页面"""

        data = response.meta

        # 2019.2.27 单独拆开 ** ----------- **** ----------- **** ----------- **** ----------- **
        for shortcode in data['shortcode']:
            if shortcode:
                video_url = "https://www.instagram.com/p/%s/" % shortcode
                yield scrapy.Request(video_url, callback=self.parse_video_detail, meta={})

        result = self.parse_js_requests(data['js_query_url'], data['csrf_token'], data['rhx_gis'])
        if result['has_next_page'] and self.loading_times < self.max_loading_times:
            yield scrapy.Request(self.transition_url(), callback=self.parse_transition_url, meta=result,
                                 dont_filter=True)
        else:
            print '加载完成 --- 加载次数: %s, 视频个数: %s' % (self.loading_times, len(self.container))
            self.save_shortcode()

    # 未弄清为啥 scrapy.Request 不能附加请求头的问题, 暂时弃用待日后研究.
    # def parse_js_response(self, response):
    #
    #     csrf_token = response.meta.get('csrf_token')
    #
    #     target_dict = json.loads(response.text)
    #     # target_dict.keys()  # [u'status', u'data']
    #
    #     # target_dict['data']['hashtag'].keys()
    #     # [u'name', u'allow_following', u'edge_hashtag_to_media', u'is_top_media_only', u'profile_pic_url',
    #     # u'is_following', u'edge_hashtag_to_content_advisory', u'edge_hashtag_to_top_posts', u'id']
    #
    #     short = target_dict['data']['hashtag']
    #     assert short['name'] == self.keyword
    #
    #     # if short['allow_following']:
    #     #     print '可以继续加载'
    #
    #     # id_ = short['id']
    #
    #     # # 热门视频: 有空再分析
    #     # top_posts = short['edge_hashtag_to_top_posts']
    #     #
    #     # for i in top_posts['edges']:
    #     #     shortcode_ = i['node']['shortcode']
    #
    #     media = short['edge_hashtag_to_media']
    #     # count = media['count']  # 相关视频的总数
    #
    #     sum_count = len(media['edges'])
    #     print '本次加载的视频个数: %s' % sum_count
    #
    #     """
    #     >>> edge_hashtag_to_media['edges'][0]['node'].keys()
    #     [u'edge_media_preview_like', u'is_video', u'edge_media_to_caption', u'dimensions', u'display_url',
    #     u'edge_media_to_comment', u'comments_disabled', u'__typename', u'owner', u'accessibility_caption',
    #     u'edge_liked_by', u'thumbnail_resources', u'taken_at_timestamp', u'thumbnail_src', u'shortcode', u'id']
    #     """
    #
    #     for i in media['edges']:
    #         shortcode = i['node']['shortcode']
    #         print shortcode
    #
    #     # 继续加载
    #     end_cursor = media['page_info']['end_cursor']
    #     if media['page_info']['has_next_page']:
    #         print '还有下一页'
    #
    #         import ipdb;ipdb.set_trace()
    #
    #         js_query_url = self.js_query_url('f92f56d47dc7a55b606908374b43a314', end_cursor)
    #         yield scrapy.Request(js_query_url,
    #                              callback=self.parse_js_response,
    #                              headers=self.headers(csrf_token, ''),
    #                              meta={'csrf_token': csrf_token}
    #                              )

    def parse_video_detail(self, response):

        response_url = unquote(response.url)
        response_url = response_url.split('url=')[-1] if 'url=' in response_url else response_url

        target = response.text.split('<script type="text/javascript">window._sharedData =')[1].split(';</script>')[0]
        target_dict = json.loads(target)
        # print target_dict.keys()

        target_dict = target_dict['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        # print target_dict.keys()

        # 配文
        try:
            text = target_dict['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            text = ''

        # 点赞数
        like_count = target_dict['edge_media_preview_like']['count']

        # 视频浏览数（图片则无该数据）
        video_view_count = target_dict.get('video_view_count')

        # 评论数
        review_count = target_dict['edge_media_to_comment']['count']

        username = target_dict['owner']['username']
        profile_url = "https://www.instagram.com/" + username + "/"

        # if self.token:
        #     profile_url = 'https://api.proxycrawl.com/?token=%s&%s&url=' % (
        #         self.token, 'country=US') + quote(profile_url)

        yield scrapy.Request(profile_url, callback=self.parse_profile,
                             meta={
                                 'username': username,
                                 'full_name': target_dict['owner']['full_name'],
                                 'post_url': response_url,

                                 'text': text,
                                 'like_count': like_count,
                                 'video_view_count': video_view_count,
                                 'review_count': review_count
                             })

    def parse_profile(self, response):

        response_url = unquote(response.url)
        response_url = response_url.split('url=')[-1] if 'url=' in response_url else response_url

        item = InstagramItem()
        meta = response.meta

        item["username"] = meta.get("username")
        item["full_name"] = meta.get("full_name")

        item["post_url"] = meta.get("post_url")
        item["text"] = meta.get("text")
        item["like_count"] = meta.get("like_count")
        item["video_view_count"] = meta.get("video_view_count")
        item["review_count"] = meta.get("review_count")

        item["profile_url"] = response_url

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

        # 或者都从这里提取数据
        target = response.text.split('<script type="text/javascript">window._sharedData =')[1].split(';</script>')[0]
        target_dict = json.loads(target)
        useful_dict = target_dict['entry_data']['ProfilePage'][0]['graphql']['user']

        item['business_phone_number'] = useful_dict.get('business_phone_number')
        item['business_email'] = useful_dict.get('business_email')
        item['is_joined_recently'] = useful_dict.get('is_joined_recently')
        item['highlight_reel_count'] = useful_dict.get('highlight_reel_count')
        item['is_business_account'] = useful_dict.get('is_business_account')
        item['full_name'] = useful_dict.get('full_name')
        item['biography'] = useful_dict.get('biography')
        item['business_address'] = useful_dict.get('business_address_json')
        item['business_category_name'] = useful_dict.get('business_category_name')
        item['following'] = useful_dict['edge_follow']['count']
        item['external_url'] = useful_dict.get('external_url')

        item['keyword'] = self.keyword

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

    def save_shortcode(self):

        file_name = '/Users/admin/Desktop/ins/%s-%s.csv' % (self.keyword,
                                                            strftime('%Y-%m-%d %H:%M:%S', localtime(time())))
        with open(file_name, u"w") as result_file:
            writer = csv.writer(result_file)
            writer.writerow(['shortcode'])
            for item in self.container:
                writer.writerow([item])

        print 'shortcode 数据存档完毕'

    @staticmethod
    def transition_url():
        """过渡用的url"""

        url = 'https://www.amazon.com/product-reviews/B01LEEWO7C?ie=UTF8&t=%s&r=%s' % (str(time())[:-3],
                                                                                       str(random.random())[2:])
        return url


class InsDeepSpider(InsSpider):

    """爬取 Instagram 关键字搜索的个人信息

    proxychains4 scrapy crawl ins_deep_spider -o travelaway-1.csv
    """

    name = "ins_deep_spider"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 100,
            'scrapy_spider.middlewares.CustomRetryMiddleware': 1000,
        },

        'FEED_EXPORT_FIELDS': [
            'username', 'full_name', 'followers', 'following', 'posts', 'highlight_reel_count', 'like_count',
            'video_view_count', 'review_count', 'business_phone_number', 'business_email', 'business_category_name',
            'business_address', 'is_business_account', 'is_joined_recently', 'biography', 'post_url', 'text',
            'external_url', 'last_online', 'profile_url', 'get_time', 'keyword'
        ]
    }

    def __init__(self, *args, **kwargs):
        super(InsDeepSpider, self).__init__(*args, **kwargs)

        self.base_start_url = 'https://www.instagram.com/p/%s/'
        self.short_code_resource = '/Users/admin/Desktop/ins/'

        self.container = []

    def start_requests(self):
        """
        https://www.instagram.com/p/BuXPcdEDGH_/
        """

        file_names = [self.short_code_resource + i + '.csv' for i in [
            'travelaway-2019-02-27 14-30-14',
            'travelaway-2019-02-27 14-36-26',
            'travelaway-2019-02-27 14-42-28',
            'travelaway-2019-02-27 14-48-52',
            'travelaway-2019-02-27 14-55-21'
        ]]

        for file_name in file_names:

            with open(file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        line_count += 1
                        self.container.append(row[0])

        for short_code in self.container:
            url = self.base_start_url % short_code

            if self.token:
                url = 'https://api.proxycrawl.com/?token=%s&%s&url=' % (self.token, 'country=US') + quote(url)

            yield scrapy.Request(url, callback=self.parse_video_detail)
