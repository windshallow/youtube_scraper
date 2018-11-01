# -*- coding: utf-8 -*-
# https://doc.scrapy.org/en/latest/topics/practices.html#run-from-script

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
# from scrapy import settings
# from scrapy_spider import settings
from scrapy.utils.project import get_project_settings
from scrapy_spider.spiders.quotes_spider import QuotesSpiderSpider
# from models import Domain  # 数据库 orm


class DomainCrawlerScript(object):

    def __init__(self):
        self.crawler = CrawlerProcess(get_project_settings())
        # self.crawler.install()
        # self.crawler.configure()

    # def _crawl(self, domain_pk):
    def _crawl(self, urls):
        # domain = Domain.objects.get(
        #     pk=domain_pk,
        # )
        # urls = []
        # for page in domain.pages.all():
        #     urls.append(page.url())
        # urls = ['http://quotes.toscrape.com/']
        print '======== 1 ========', urls, type(urls)
        self.crawler.crawl(QuotesSpiderSpider(urls))
        self.crawler.start()
        self.crawler.stop()

    # def crawl(self, domain_pk):
    #     p = Process(target=self._crawl, args=[domain_pk])
    #     p.start()
    #     p.join()

    # def crawl(self, urls):
    #     p = Process(target=self._crawl, args=[urls])
    #     p.start()
    #     p.join()


crawler = DomainCrawlerScript()


# def domain_crawl(domain_pk):
#     crawler.crawl(domain_pk)

def domain_crawl(urls):
    # crawler.crawl(urls)
    crawler._crawl(urls)

