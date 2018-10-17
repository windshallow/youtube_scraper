# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from scrapy_spider.models import QuoteDB, db_connect, create_table, YoutubeCelebrityInfoDB


class ScrapySpiderPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        quotedb = QuoteDB()
        quotedb.quote = item["quote"]
        quotedb.author = item["author"]

        try:
            session.add(quotedb)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class YoutubeCelebrityInfoPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        youtube_db = YoutubeCelebrityInfoDB()
        youtube_db.keyword = item["keyword"]
        youtube_db.name = item["name"]
        youtube_db.homepage_link = item["homepage_link"]
        youtube_db.description = item["description"]
        youtube_db.mail_string = item["mail_string"]
        youtube_db.link_string = item["link_string"]
        # youtube_db.subscriber_count = item["subscriber_count"]
        # youtube_db.view_count = item["view_count"]
        # youtube_db.joined_date = item["joined_date"]
        youtube_db.country = item["country"]
        # youtube_db.other_contact = item["other_contact"]
        youtube_db.google = item["google"]
        youtube_db.twitter = item["twitter"]
        youtube_db.facebook = item["facebook"]
        youtube_db.instagram = item["instagram"]
        youtube_db.website = item["website"]

        try:
            session.add(youtube_db)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
