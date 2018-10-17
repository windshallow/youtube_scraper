# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class QuoteItem(Item):
    author = Field()
    quote = Field()


class YoutubeCelebrityInfoItem(Item):

    """ 基于 关键字 搜索YouTube上, 视频发布者的个人信息 """

    keyword = Field()
    name = Field()
    homepage_link = Field()
    description = Field()
    mail_string = Field()
    link_string = Field()
    subscriber_count = Field()
    view_count = Field()
    joined_date = Field()
    country = Field()
    other_contact = Field()
    google = Field()
    twitter = Field()
    facebook = Field()
    instagram = Field()
    website = Field()
