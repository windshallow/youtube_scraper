# -*- coding: utf-8 -*-

from app import celery


@celery.task()
def crawl_domain(domain_pk):
    from crawl import domain_crawl
    return domain_crawl(domain_pk)
