# -*- coding: utf-8 -*-

from flask import Flask, request
from celery import Celery
from crawl import domain_crawl


import subprocess
from time import sleep


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # redis
# app.config['CELERY_RESULT_BACKEND'] = 'amqp://guest@localhost//'  # mq
# app.config['CELERY_RESULT_BACKEND'] = 'db+postgresql://scott:tiger@localhost/mydatabase'  # postgresql
# app.config['CELERY_RESULT_BACKEND'] = 'db+postgresql+psycopg2://admin:@127.0.0.1:5432/admin'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def index():
    return 'hello world'


# ----------------------------------------------- 通过 flask 的 /celery_test 接口调用celery 的 add 任务
# cd ~/Desktop/funny/youtube_scraper    # cd ~/funny/youtube_scraper    # MacBook Pro
# celery worker -A app.celery -l INFO   开启worker，监听队列， -A参数指向 Celery类的实例的位置
# python app.py                         另开终端，同目录下启动flask服务
# 打开浏览器访问： http://127.0.0.1:5000/celery_test   即可触发celery任务


@celery.task
def add(x, y):
    sleep(4)
    return x + y


@app.route('/celery_test')
def celery_test():
    add.delay(4, 8)  # delay方法可触发 celery 任务 ！！！
    return 'starting'


# http://127.0.0.1:5000/calculate?x=3&y=4
@app.route('/calculate')
def calculate():
    x = int(request.args.get('x', 1))
    y = int(request.args.get('y', 1))
    res = add.delay(x, y)
    print res, type(res), dir(res)
    print res.result, type(res)  # 异步任务的结果是存在其他地方的，通常也不会用到结果值。【顶多成功与否发个信号】
    return 'starting calculate'


@celery.task
def hostname():
    return subprocess.check_output(['hostname'])


# --------------------------------------------

@celery.task()
def crawl_domain(urls):
    # from crawl import domain_crawl
    return domain_crawl(urls)


@app.route('/crawler')
def crawler():
    urls = 'http://quotes.toscrape.com/'
    crawl_domain.delay(urls)
    print '运行结束'
    return '开始爬虫'

# 从作为backend的redis中将结果取出来，代码如下
# 参考： https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-apa-chong-kong-qi-zhi-liang-he-fen-bu-shi
# import redis
# import json
#
# r = redis.Redis(host='localhost',port=6379,db=0)
#
# failure = []
# keys = r.keys()
# for key in keys:
#     res = r.get(key)
#     try:
#         res = json.loads(res.decode('utf-8'))
#     except ValueError:
#         failure.append(key)
#     else:
#         print res
#         print keys.index(key), '==='


if __name__ == '__main__':
    app.run(debug=True)
