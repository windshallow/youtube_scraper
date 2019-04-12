# -*- coding: utf-8 -*-
import scrapy
from scrapy_spider.items import QuoteItem


class QuotesSpiderSpider(scrapy.Spider):

    """
    $ scrapy crawl quotes_spider -a url=http://quotes.toscrape.com/ -s CLOSESPIDER_ITEMCOUNT=90

    注解:
        -s CLOSESPIDER_ITEMCOUNT=90 : item 个数为90个的时候终止爬虫。
    """

    name = 'quotes_spider'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'scrapy_spider.pipelines.ScrapySpiderPipeline': 300,
            # 'scrapy_spider.pipelines.es.EsWriterPipeline': 800,
            # 'scrapy_spider.pipelines.es_2.EsWriterPipeline': 800,
            # 'scrapy_spider.pipelines.psql.PostgreSQLWriterPipeline': 801,
            'scrapy_spider.pipelines.orm_postgre.AddTablePipeline': 802,
        }
    }

    def __init__(self, url, *args, **kwargs):
        super(QuotesSpiderSpider, self).__init__(*args, **kwargs)
        # self.start_urls = url  # list
        self.start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")

        for quote in quotes:
            item = QuoteItem()
            item["quote"] = quote.xpath(".//span[@class='text']/text()").extract_first()
            item["author"] = quote.xpath(".//small//text()").extract_first()
            yield item

        next_page_url = response.xpath("//li[@class='next']//a/@href").extract_first()
        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url)
