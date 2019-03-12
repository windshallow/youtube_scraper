# -*- coding: utf-8 -*-
"""
© 2018 QYT Technology
Authored by: Lin Renwei (931798845@qq.com)

"""

import re
import scrapy
import urlparse

from scrapy_spider import settings
from scrapy_spider.items import YoutubeCelebrityInfoItem
from scrapy_spider.utils.date_clean import date_change
from scrapy_spider.utils.url_processor import update_url_param, clean_url_param


class YoutubeCelebrityInfoSpider(scrapy.Spider):

    """  根据keyword搜索YouTube红人视频, 抓取红人信息

    proxychains4 scrapy crawl youtube_celebrity_info -a page_limit=2 -a keyword='bath+mat+review' -o a.json

    proxychains4 scrapy crawl youtube_celebrity_info -a page_limit=2 -a keyword='bath+mat+review' -a csv=1 -o a.csv

    """

    name = "youtube_celebrity_info"
    allowed_domains = ["youtube.com"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapy_spider.middlewares.ProxyMiddleare': 544,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 100,
            'scrapy_spider.middlewares.CustomRetryMiddleware': 1000,
            'scrapy_spider.middlewares.RotateUserAgentMiddleware': 543,
            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 666,
            # 'scrapy_crawlera.CrawleraMiddleware': 610
        },
        # 'CRAWLERA_ENABLED': True,
        # 'CRAWLERA_APIKEY': '854fbe371c13433b871ece7923163875',

        'FEED_EXPORT_FIELDS': [
            'name', 'subscriber_count', 'view_count', 'mail_string', 'link_string', 'google', 'twitter', 'facebook',
            'instagram', 'website', 'country', 'joined_date', 'description', 'other_contact', 'homepage_link', 'keyword'
        ],
        'ITEM_PIPELINES': {
            # 'scrapy_spider.pipelines.YoutubeCelebrityInfoPipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):

        super(YoutubeCelebrityInfoSpider, self).__init__(*args, **kwargs)

        self.task_id = kwargs.get('task_id', '')
        self.action_type = kwargs.get('action_type', '')

        self.export_csv = kwargs.get('csv', False)  # 默认导出JSON, 而不是CSV格式的数据
        self.page_limit = kwargs.get('page_limit', 1)
        if isinstance(self.page_limit, str):
            self.page_limit = self.page_limit.strip()
        self.page_limit = int(self.page_limit)
        self.page = 1  # 采用next_page 方式时为 0

        self.country_code = kwargs.get('country_code', u'US').upper()
        keyword = kwargs.get('keyword', u'beach+tent+review')
        if isinstance(keyword, str):
            keyword = keyword.decode(u'utf-8')
        self.keyword = keyword.strip().replace(u' ', u'+')
        self.filter = kwargs.get('filter', u'')  # 默认不过滤搜索结果

    def start_requests(self):

        """ https://www.youtube.com/results?search_query=beach+tent+review&gl=US """

        # 抓取单个 关键字 的红人信息
        # url = u'https://www.youtube.com/results'
        # param_dict = {u'search_query': self.keyword, u'gl': self.country_code}  # {u'sp': self.filter}
        # start_url = update_url_param(url, param_dict)
        url = u'https://www.youtube.com/results?search_query=%s&gl=%s'
        start_url = url % (self.keyword, self.country_code)
        yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response):
        # 未考虑 0 结果的
        result_number_list = response.xpath(u'//*[@class="num-results first-focus"]/text()').extract()
        if result_number_list:
            result_number = re.findall(r'(\d+)', result_number_list[0].replace(u',', u''))[0]
            print u'\n\n数据总数为: %s\n\n' % result_number

        all_results = response.xpath(u'//ol[@class="item-section"]/li')
        for result in all_results:
            try:
                name = result.xpath(u'.//div[@class="yt-lockup-byline "]/a/text()').extract()[0]
                print u'名字为: %s\n' % name
                link = result.xpath(u'.//div[@class="yt-lockup-byline "]/a/@href').extract()[0]
                homepage_link = urlparse.urljoin(response.url, link) + u'/about'
                print u'个人主页url为: %s\n' % homepage_link

                yield scrapy.Request(homepage_link, callback=self.parse_about,
                                     meta={u'name': name, u'homepage_link': homepage_link})
            except IndexError:
                print u'该条数据为无效信息'
                continue

        # --------------------------------------------------------------------------------------------------------------

        self.page += 1
        if self.page <= self.page_limit:
            next_page_url = update_url_param(response.url, {u'page': self.page})

            print u'开始爬取下一页: ', next_page_url

            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_about(self, response):

        item = YoutubeCelebrityInfoItem()

        item['keyword'] = self.keyword
        item['name'] = response.meta[u'name']
        item['homepage_link'] = response.meta[u'homepage_link']

        try:
            description = response.xpath(
                u'//div[@class="about-description branded-page-box-padding"]/pre/text()').extract()[0].strip()
        except IndexError:
            description = u''
        item['description'] = description.replace(u'\n', u'')
        print description

        mail_in_description = re.findall(r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)', description)
        mail_list = [i[0] for i in mail_in_description]
        mail_string = u' ,  '.join(mail_list)
        item['mail_string'] = mail_string
        print mail_string

        link_in_description = re.findall(r'(https*:\S+)', description)
        link_string = u' ,  '.join(link_in_description)
        item['link_string'] = link_string
        print link_string

        # --------------------------------------------------------------------------------------------------------------

        try:
            subscriber_count = int(response.xpath(
                u'//div[@class="about-stats"]/span[1]/b/text()').extract()[0].replace(u',', u'').strip())
        except IndexError:
            subscriber_count = None
        item['subscriber_count'] = subscriber_count
        print subscriber_count

        try:
            view_count = int(response.xpath(
                u'//div[@class="about-stats"]/span[2]/b/text()').extract()[0].replace(u',', u'').strip())
        except IndexError:
            view_count = None
        item['view_count'] = view_count
        print view_count

        month_dict = {u'Jan': u'Jan', u'Feb': u'Feb', u'Mar': u'Mar', u'Apr': u'Apr', u'May': u'May', u'Jun': u'Jun',
                      u'Jul': u'Jul', u'Aug': u'Aug', u'Sep': u'Sep', u'Oct': u'Oct', u'Nov': u'Nov', u'Dec': u'Dec'}

        try:
            joined_date_text = response.xpath(
                u'//div[@class="about-stats"]/span[3]/text()').extract()[0].replace(u'Joined', u'').strip()
        except IndexError:
            joined_date_text = None

        if joined_date_text:
            joined_date = date_change(joined_date_text, month_dict)
            item['joined_date'] = joined_date
            print joined_date

        # --------------------------------------------------------------------------------------------------------------

        try:
            country = response.xpath(u'//span[@class="country-inline"]/text()').extract()[0].strip()
        except IndexError:
            country = None
        item['country'] = country
        print country

        # --------------------------------------------------------------------------------------------------------------

        try:
            custom_links = response.xpath(
                u'//div[@class="about-metadata branded-page-box-padding clearfix "]/ul[@class="about-custom-links"]/li')
        except IndexError:
            custom_links = None

        other_contact = None
        link_list, title_list = [], []
        if custom_links:
            for link in custom_links:
                url = link.xpath(u'./a/@href').extract()[0]
                url = urlparse.urljoin(response.url, url)
                if u'q=' in url:
                    new_url = clean_url_param(url)[1].get(u'q')
                else:
                    new_url = url
                link_list.append(new_url)
                print new_url
                title = link.xpath(u'./a/@title').extract()[0].strip().replace(u' ', u'_').lower()
                title_list.append(title)
                print title
            other_contact = dict(zip(title_list, link_list))
            item['other_contact'] = other_contact

        keyword_list = [u'google', u'twitter', u'facebook', u'instagram', u'website']

        if other_contact:
            self.other_contact_sep(keyword_list, other_contact, item)

        # --------------------------------------------------------------------------------------------------------------

        yield item

        # task = create_task_data(self.name, self.task_id, self.action_type, item,
        #                         YoutubeWebCelebrityInformationTask)
        #
        # if self.export_csv:
        #     yield item         # 导出CSV格式数据
        # else:
        #     yield task         # 导出JSON格式数据

    @staticmethod
    def other_contact_sep(keyword_list, contact_dict, item):

        for keyword in keyword_list:
            for key in contact_dict:
                if keyword in key:
                    item[keyword] = contact_dict.get(key)
        return item


