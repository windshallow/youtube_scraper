# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime, Text
from scrapy_spider.spiders.database.connection import Base


class QuoteModel(Base):

    __tablename__ = "quote"

    id = Column(Integer, primary_key=True)
    author = Column('author', String(100))
    quote = Column('quote', Text())

    def __init__(self, _id=None, author=None, quote=None):
        self.id = _id
        self.author = author
        self.quote = quote

    def __repr__(self):
        return "<QuoteModel: id='%s', author='%s', quote='%s'>" % (self._id, self.author, self.quote)
