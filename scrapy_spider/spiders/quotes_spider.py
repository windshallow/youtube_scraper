# -*- coding: utf-8 -*-
import scrapy
from scrapy_spider.items import QuoteItem


class QuotesSpiderSpider(scrapy.Spider):
    name = 'quotes_spider'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_spider.pipelines.ScrapySpiderPipeline': 300,
        }
    }

    def __init__(self, url, *args, **kwargs):
        super(QuotesSpiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = url  # list

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath(
                ".//span[@class='text']/text()").extract_first()
            author = quote.xpath(
                ".//small//text()").extract_first()

            item = QuoteItem()
            item["quote"] = text
            item["author"] = author
            print author

            yield item

        next_page_url = response.xpath("//li[@class='next']//a/@href").extract_first()
        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url)
