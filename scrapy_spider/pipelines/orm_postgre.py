# -*- coding: utf-8 -*-

from scrapy_spider.spiders.database.connection import db
from scrapy_spider.spiders.database.models import QuoteModel


class AddTablePipeline(object):

    def open_spider(self, spider):
        print("先创建表")

    def process_item(self, item, spider):
        if item['author'] and item['quote']:

            record = QuoteModel(
                author=item['author'].decode('unicode_escape'),
                quote=item['quote']
            )

            db.add(record)
            db.commit()
            return item

    def close_spider(self, spider):
        db.close()
