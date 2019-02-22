# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import datetime
import hashlib
import json
import re
import scrapy
from urllib import quote
from collections import OrderedDict
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
            # 'scrapy_spider.middlewares.RotateUserAgentMiddleware': 543,
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

    @staticmethod
    def cookie(csrftoken):

        cookie = {
            'rur': 'FRC',
            'mid': 'XGYzZAAEAAE4S_MNDivha2fkaI7s',
            'csrftoken': csrftoken,
            'ds_user_id': '11168392113',
            'sessionid': '11168392113%3A51cZNjbvVfyt1p%3A10',
            'urlgen': '"{\"95.169.14.232\": 25820}:1gwi7Q:Pbk2T58XBuljTG9wEj94ODVaddc"',
        }
        sequence = ['rur', 'mid', 'csrftoken', 'ds_user_id', 'sessionid', 'urlgen']
        cookie = ''.join([k + '=' + cookie[k] + '; ' for k in sequence])[: -2]

        return cookie

    @property
    def user_agent(self):
        return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
               'Chrome/72.0.3626.109 Safari/537.36'

    def x_instagram_gis(self, query_variables, rhx_gis):

        """创建签名
        https://stackoverflow.com/questions/49786980/how-to-perform-unauthenticated-instagram-web-scraping-in-response-to-recent-priv
        """

        # query_variables = '%7B%22tag_name%22%3A%22football%22%2C%22show_ranked%22%3Afalse%2C%22first%22%3A10%2C%22after%22%3A%22QVFCSXhZYWtiZnA0VHZCYmFoaVRQN0J1UUpJcW1iSTctNTZPYXVQc2JHVTdtSHlVU3RWOXZNcGFWcWtXOGVsT21ab3VhTEZ6T2doMHVtb1RLM0NDS204Tg%3D%3D%22%7D'
        # rhx_gis = 'e929e57cbe8e65b202c6e5d8f808d644'
        md5 = hashlib.md5()
        md5.update(json.dumps({rhx_gis: query_variables}))
        x_instagram_gis = md5.hexdigest()
        return x_instagram_gis

    def headers(self, csrftoken):

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6',
            'cache-control': 'no-cache',
            'cookie': self.cookie(csrftoken),
            'pragma': 'no-cache',
            'referer': 'https://www.instagram.com/explore/tags/%s/' % self.keyword,
            'user-agent': self.user_agent,
            'x-ig-app-id': '936619743392459',  # 貌似不会变用同一台机器抓的时候
            'x-instagram-gis': 'e929e57cbe8e65b202c6e5d8f808d644',
            'x-requested-with': 'XMLHttpRequest',
        }

        return headers

    def js_query_url(self, query_hash, end_cursor):
        """动态加载url"""

        table = OrderedDict([
            ("tag_name", self.keyword),
            ("show_ranked", False),
            ("first", 12),
            ("after", end_cursor)
        ])
        query_string_parameters = quote(json.dumps(table, sort_keys=False).replace(' ', ''))  # key有排序

        url = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={variables}'.format(
            query_hash=query_hash, variables=query_string_parameters
        )
        return url

    def parse(self, response):

        target = response.text.split('<script type="text/javascript">window._sharedData =')[1].split(';</script>')[0]
        # target = response.text  # js
        target_dict = json.loads(target)

        # print target_dict.keys()
        csrf_token = target_dict['config']['csrf_token']
        rhx_gis = target_dict['rhx_gis']

        hashtag = target_dict['entry_data']['TagPage'][0]['graphql']['hashtag']
        # print hashtag.keys()

        # id_ = hashtag['id']

        for obj_ in hashtag['edge_hashtag_to_media']['edges']:
            obj = obj_['node']
            # print obj.keys()

            # display_url = obj['display_url']  # 视频主图
            # owner_id = obj['owner']['id']  # 视频发布者的id
            # taken_at_timestamp = obj['taken_at_timestamp']  # 视频发布时间戳
            shortcode = obj['shortcode']  # 可构造视频详情页url
            # video_id = obj['id']  # 猜测是视频的id

            # if shortcode:
            #     video_url = "https://www.instagram.com/p/%s/" % shortcode
            #     yield scrapy.Request(video_url, callback=self.parse_video_detail, meta={})

        # 动态加载
        page_info = hashtag['edge_hashtag_to_media']['page_info']
        end_cursor = page_info['end_cursor']
        if page_info['has_next_page'] and self.loading_times < self.max_loading_times:
            self.loading_times += 1
            print '\n开始第%s次加载\n' % self.loading_times

            js_query_url = self.js_query_url('f92f56d47dc7a55b606908374b43a314', end_cursor)
            print js_query_url, '========js_query_url========'
            print '\n'
            import ipdb;ipdb.set_trace()
            yield scrapy.Request(js_query_url, callback=self.parse_js_response, headers=self.headers(csrf_token),
                                 meta={'csrf_token': csrf_token})
        #     yield scrapy.Request(js_query_url, callback=self.parse, headers=self.headers())
        # else:
        #     print '加载完成 --- 加载次数: ', self.loading_times

    def parse_js_response(self, response):

        # todo 待解析出 csrftoken
        csrftoken = response.headers['Set-Cookie']
        # 'csrftoken=FLhU21raeQ6QDehYPW6OwER9YmVKWLlp; Domain=.instagram.com; expires=Fri, 21-Feb-2020 03:18:41 GMT; Max-Age=31449600; Path=/; Secure'

        target_dict = json.loads(response.text)
        # target_dict.keys()  # [u'status', u'data']

        # target_dict['data']['hashtag'].keys()
        # [u'name', u'allow_following', u'edge_hashtag_to_media', u'is_top_media_only', u'profile_pic_url',
        # u'is_following', u'edge_hashtag_to_content_advisory', u'edge_hashtag_to_top_posts', u'id']

        short = target_dict['data']['hashtag']
        assert short['name'] == self.keyword

        # if short['allow_following']:
        #     print '可以继续加载'

        id_ = short['id']
        top_posts = short['edge_hashtag_to_top_posts']  # 热门视频

        for i in top_posts['edges']:
            shortcode_ = i['node']['shortcode']

        media = short['edge_hashtag_to_media']
        count = media['count']  # 相关视频的总数

        sum_count = len(media['edges'])
        print '本次加载的视频个数: %s' % sum_count

        """
        >>> edge_hashtag_to_media['edges'][0]['node'].keys()
        [u'edge_media_preview_like', u'is_video', u'edge_media_to_caption', u'dimensions', u'display_url', 
        u'edge_media_to_comment', u'comments_disabled', u'__typename', u'owner', u'accessibility_caption', 
        u'edge_liked_by', u'thumbnail_resources', u'taken_at_timestamp', u'thumbnail_src', u'shortcode', u'id']
        """

        for i in media['edges']:
            shortcode = i['node']['shortcode']
            print shortcode

        # 继续加载
        end_cursor = media['page_info']['end_cursor']
        if media['page_info']['has_next_page']:
            print '还有下一页'
            js_query_url = self.js_query_url('f92f56d47dc7a55b606908374b43a314', end_cursor)
            yield scrapy.Request(js_query_url,
                                 callback=self.parse_js_response, headers=self.headers(response.meta['csrf_token']))

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
