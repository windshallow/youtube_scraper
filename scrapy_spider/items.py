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


class MobileUserAgentItem(Item):
    """
    移动端用户代理
    """

    user_agent = Field()
    software = Field()
    software_type = Field()
    os = Field()
    popularity = Field()


class SlickDealsItem(Item):

    user_name = Field()
    joined = Field()
    title = Field()
    posts = Field()
    reputation = Field()
    date_time = Field()
    post_number = Field()
    content = Field()
    email = Field()
    up_vote = Field()
    down_vote = Field()
    profile = Field()


class InstagramItem(Item):
    pk = Field()
    username = Field()
    full_name = Field()
    is_private = Field()
    profile_pic_url = Field()
    profile_pic_id = Field()
    is_verified = Field()
    has_anonymous_profile_picture = Field()
    # follower_count = Field()
    reel_auto_archive = Field()
    # byline = Field()
    mutual_followers_count = Field()
    unseen_count = Field()

    profile_url = Field()

    followers = Field()
    following = Field()
    posts = Field()
    external_url = Field()
    last_online = Field()

    get_time = Field()

    business_phone_number = Field()
    business_email = Field()
    is_joined_recently = Field()
    highlight_reel_count = Field()
    is_business_account = Field()
    biography = Field()
    business_address = Field()
    business_category_name = Field()

    keyword = Field()

    post_url = Field()
    text = Field()
    like_count = Field()
    video_view_count = Field()
    review_count = Field()
