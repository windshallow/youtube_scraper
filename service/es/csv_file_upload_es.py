# -*- coding:utf-8 -*-
import csv
import sys
import os
import logging
import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# 禁用：https://blog.ernest.me/post/python-setdefaultencoding-unicode-bytes
# reload(sys)
# sys.setdefaultencoding('utf8')


logging.basicConfig()
es = Elasticsearch()


def import_csv(index_name, type_name, file_name):
    if not os.path.exists(file_name):
        print("file not found")
        return

    actions = []
    if not es.indices.exists(index=index_name, allow_no_indices=True):
        # print "not found index"
        es.indices.create(index=index_name, body={}, ignore=400)

    for item in csv.DictReader(open(file_name, 'rb')):
        actions.append({"_index": index_name, "_type": type_name, "_source": encoding(item)})
    res = helpers.bulk(es, actions, chunk_size=1000)
    es.indices.flush(index=[index_name])
    return len(actions)


def encoding(item):
    for i in item:
        # item[i] = str(item[i]).encode('utf-8')  # old
        item[i] = str(item[i]).decode('utf-8')
    return item


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    result = import_csv("amazon_node_tree", "doc", "/Users/admin/Desktop/amazon_node_tree.csv")
    print("import size = " + str(result))
    end_time = datetime.datetime.now()
    print("import cost = " + str(end_time - start_time))
