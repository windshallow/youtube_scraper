# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import scrapy
from dateparser import parse

from scrapy_spider.items import SlickDealsItem


class SlickDealsSpider(scrapy.Spider):

    """爬取 slickdeals 的商品评论信息

    proxychains4 scrapy crawl slick_deals -o slickdeals.csv
    """

    name = "slick_deals"
    allowed_domains = ["slickdeals.net"]
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
        super(SlickDealsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """
        https://slickdeals.net/f/5276432-freedompop-friends?page=1
        """
        for i in range(1, 3):  # 462
            url = 'https://slickdeals.net/f/5276432-freedompop-friends?page=%s' % i
            yield scrapy.Request(url)

    def parse(self, response):

        for i in response.xpath('//*[@id="posts"]//*[@class="postReplyContainer"]'):
            item = SlickDealsItem()

            item['user_name'] = self.cleaner(i.xpath(
                './/*[@class="postUsername"]//*[@class="usernameButton buttonUnstyled"]//text()'), index=0)

            item['joined'] = parse(self.cleaner(i.xpath('.//*[@class="posterJoined"]/text()'), -1, ['Joined']))

            item['title'] = self.cleaner(i.xpath('.//*[@class="posterTitle"]/span[2]/text()'), index=0)

            item['posts'] = self.cleaner(i.xpath('.//*[@class="numPosts"]//text()'), -1, ['Posts', ',', '#'])

            item['reputation'] = self.cleaner(
                i.xpath('.//*[@class="posterRep"]//*[@class="reputation_value"]/text()'), 0, [','])

            item['date_time'] = ''.join([x.strip() for x in self.cleaner(
                i.xpath('.//*[@class="postText"]//*[@class="postDateTime"]//text()')
            ) if x.strip()]).replace('at', ' at ')

            item['post_number'] = self.cleaner(
                i.xpath('.//*[@class="postNumber postPermalink"]/text()'), index=0, replace_list=['#', ','])

            item['content'] = ''.join(self.cleaner(i.xpath('.//*[@class="postTextContent"]//text()'))).replace(
                '\n', '').strip()

            item['email'] = self.cleaner(i.xpath('.//*[@class="postTextContent"]//a/text()'))

            item['up_vote'] = self.cleaner(
                i.xpath('.//*[@class="postTextBottom"]//*[@class="postUpVote"]/text()'), index=0)

            item['down_vote'] = self.cleaner(
                i.xpath('.//*[@class="postTextBottom"]//*[@class="postDownVote"]/text()'), index=0)

            item['profile'] = self.cleaner(i.xpath('.//*[@class="dropdown-menu"]//input/@value'), index=0)

            yield item

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
