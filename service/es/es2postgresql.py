# -*- coding: utf-8 -*-
import arrow
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from sqlalchemy import create_engine, Numeric, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

es = Elasticsearch(hosts=['http://localhost:29200'])

# an Engine, which the Session will use for connection
# resources
engine = create_engine('postgresql://')
# create a configured "Session" class
Session = sessionmaker(bind=engine)
# create a Session
session = Session()

# work with sess
Base = declarative_base()

written = 0


class AmazonProduct(Base):
    __tablename__ = 'amazon_product'
    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    asin = Column(String)
    title = Column(String)
    price = Column(Numeric(12, 6))
    offers_count = Column(Integer)
    review_count = Column(Integer)
    brand = Column(String)
    seller = Column(String)
    fulfillment_channel = Column(String)
    best_sellers_rank = Column(Integer)
    best_sellers_category = Column(String)
    node_id = Column(BigInteger)
    image_main = Column(String)
    scraped_time = Column(DateTime(timezone=True))
    country = Column(String)
    __table_args__ = {
        'schema': 'scrapper'
    }


# Base.metadata.create_all(bind=engine)

size = 1000
buffer = []
node_ids = [
    1258595011,
    10208056011,
    2204506011,
    3401301,
    3400371,
    3418761,
    3422251,
    3406281,
    1265458011,
    2371054011,
]
for hit in scan(es,
                # query={"query": {
                #     "terms": {"node": node_ids}
                # }},
                index="goblin-data-amazon_product-2018.11.16",
                size=size):
    # print(json.dumps(hit, indent=2))
    src = hit['_source']
    best_sellers_rank = None
    best_sellers_category = None

    for rank in src['best_sellers_rank']:
        if rank['level'] == 1:
            best_sellers_rank = rank['rank']
            best_sellers_category = rank['category'][0]
            break

    buffer.append({
        'rank': src['data_result_rank'],
        'image': src['image_main'],
        'node_id': src['node'],
        'asin': src['asin'],
        'title': src['title'],
        'price': src['price'],
        'offers_count': src['offers_count'],
        'review_count': src['review_count'],
        'brand': src['brand'],
        'seller': src['seller'],
        'fulfillment_channel': src['fulfillment_channel'],
        'best_sellers_rank': best_sellers_rank,
        'best_sellers_category': best_sellers_category,
        'image_main': src['image_main'],
        'scraped_time': arrow.now().datetime,
        'country': src['country']

    })
    if len(buffer) == size:
        session.bulk_insert_mappings(AmazonProduct.__mapper__, buffer)
        session.commit()
        written += len(buffer)
        buffer = []
        print('written %s entries' % written)
session.bulk_insert_mappings(AmazonProduct.__mapper__, buffer)
session.commit()
written += len(buffer)
buffer = []
print('written %s entries' % written)
