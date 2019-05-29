# -*- coding:utf-8 -*-

# script_based_sorting  基于脚本的排序
# https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-sort.html#_script_based_sorting
import random

from service.es.csv_file_upload_es import es

body = {
    "query": {
        "bool": {
            "must": [
                {"term": {"country_code.keyword": "UK"}},
                ],
            "must_not": [],
            "should": []
            }
        },
    "from": 0,
    "size": 100,
    "sort": [{
        "_script": {
            "type": "number",
            "script": {
                "lang": "painless",
                "source": "doc['rank'].value * params.factor",
                "params": {
                    "factor": 1.1
                }
            },
            "order": "asc"
        }
    }],
    "aggs": {}
}

for i in es.search('bestseller', 'doc', body=body)['hits']['hits']:
    print(i['_source']['rank'])

rank_list = sorted(list(range(1, 101)), key=lambda x: x * random.random())[:10]


# *********************************************

body = {
  "query": {
    "bool": {
      "must": [
        {"term": {"country_code.keyword": "UK"}},
      ],
      "must_not": [],
      "should": []
    }
  },
  "from": 0,
  "size": 10,
  "sort": [
    {"rank": "asc"},  # 按rank 升序
    ],
  "aggs": {}
}
