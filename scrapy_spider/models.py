#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)
    # metadata = MetaData(engine)
    # metadata.create_all()


class QuoteDB(DeclarativeBase):
    __tablename__ = "quote_table"

    id = Column(Integer, primary_key=True)
    quote = Column('quote', Text())
    author = Column('author', String(100))


class YoutubeCelebrityInfoDB(DeclarativeBase):
    __tablename__ = "youtube_celebrity_info_table"

    id = Column(Integer, primary_key=True)
    keyword = Column('keyword', String(100))
    name = Column('name', String(100))
    homepage_link = Column('homepage_link', String(100))
    description = Column('description', Text())
    mail_string = Column('mail_string', String(100))
    link_string = Column('link_string', String(100))
    # subscriber_count = Column('subscriber_count', String(100))
    # view_count = Column('view_count', String(100))
    # joined_date = Column('joined_date', String(100))
    country = Column('country', String(100))
    # other_contact = Column('other_contact', String(100))
    google = Column('google', String(100))
    twitter = Column('twitter', String(100))
    facebook = Column('facebook', String(100))
    instagram = Column('instagram', String(100))
    website = Column('website', String(100))
