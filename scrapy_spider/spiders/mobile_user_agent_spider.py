# -*- coding: utf-8 -*-
import scrapy
from urllib import quote
from scrapy_spider.items import MobileUserAgentItem


class MobileUserAgentSpider(scrapy.Spider):
    """移动端用户代理
    proxychains4 scrapy crawl mobile_user_agent -o mobile_user_agent.json
    """

    name = "mobile_user_agent"
    allowed_domains = ["developers.whatismybrowser.com"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 100,
            'scrapy_spider.middlewares.CustomRetryMiddleware': 1000,
            'scrapy_spider.middlewares.RotateUserAgentMiddleware': 543,
        },
        'FEED_EXPORT_FIELDS': [
            'user_agent', 'software', 'software_type', 'os', 'popularity'
        ],
    }

    def __init__(self, *args, **kwargs):
        super(MobileUserAgentSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """
        https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/1
        """

        base_url = 'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/%s'
        for page_number in range(1, 12):
            start_url = base_url % page_number
            start_url = self.proxy_crawl_api(start_url)
            yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response):

        all_selectors = response.xpath(
            '//table[@class="table table-striped table-hover table-bordered table-useragents"]//tbody//tr'
        )
        for selector in all_selectors:
            item = MobileUserAgentItem()
            item['user_agent'] = selector.xpath('./td[@class="useragent"]/a/text()').extract()[0]
            item['software'] = selector.xpath('./td[2]/text()').extract()[0]
            item['software_type'] = selector.xpath('./td[3]/text()').extract()[0]
            item['os'] = selector.xpath('./td[4]/text()').extract()[0]
            item['popularity'] = selector.xpath('./td[5]/text()').extract()[0]
            yield item

    # 代理接口
    prefix = ''

    def proxy_crawl_api(self, url):
        """将目标url转换成适配proxy crawl这个代理的url格式, 传入完整的url"""

        url = url if isinstance(url, str) else url.encode('utf8')
        proxy_crawl_url = self.prefix + quote(url)
        return proxy_crawl_url
