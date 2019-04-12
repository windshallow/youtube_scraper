# -*- coding: utf-8 -*-
"""
How to run scrapers programmatically from a script
"""

from scrapy_spider.spiders.quotes_spider import QuotesSpiderSpider
from scrapy_spider.spiders.youtube_celebrity_info import YoutubeCelebrityInfoSpider

# scrapy api
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings


# list of crawlers
TO_CRAWL = [QuotesSpiderSpider, YoutubeCelebrityInfoSpider]

# list of crawlers that are running
RUNNING_CRAWLERS = []


def spider_closing(__spider__):
    """Activates on spider closed signal"""
    log.msg("Spider closed: %s" % __spider__, level=log.INFO)
    RUNNING_CRAWLERS.remove(__spider__)
    if not RUNNING_CRAWLERS:
        reactor.stop()


# log.start(loglevel=log.DEBUG)
for spider in TO_CRAWL:
    settings = Settings()

    # crawl responsibly
    settings.set("USER_AGENT", "Kiran Koduru (+http://kirankoduru.github.io)")

    # Add to items pipelines
    settings.set("ITEM_PIPELINES", {'pipelines.AddTablePipeline': 100})

    crawler = Crawler(settings)
    crawler_obj = spider()
    RUNNING_CRAWLERS.append(crawler_obj)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(crawler_obj)
    crawler.start()

# blocks process so always keep as the last statement
reactor.run()
