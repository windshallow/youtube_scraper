# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import requests
import time
import os
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
# driver = webdriver.Chrome(chrome_options=options)
driver = {}  # todo httplib.BadStatusLine: '' 暂时这么处理这个报错，执行其他爬虫时

target = "https://www.instagram.com/mirei_kiritani_/"

# url_set = set([])

driver.get(target)

url_set = set([])  # set用来unique URL

pic_index = 0

url_set_size = 0

# save_dir = './pic/'
save_dir = '/Users/admin/Desktop/html'

if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# requests header最好设置一下，否则服务器可能会拒绝访问
header = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'shbid=4419; rur=PRN; mcd=3; mid=W1E7cAALAAES6GY5Dyuvmzfbywic; csrftoken=uVspLzRYlxjToqSoTlf09JVaA9thPkD0; urlgen="{\"time\": 1532050288\054 \"2001:da8:e000:1618:e4b8:8a3d:8932:2621\": 23910\054 \"2001:da8:e000:1618:6c15:ccda:34b8:5dc8\": 23910}:1fgVTv:SfLAhpEZmvEcJn0037FXFMLJr0Y"',
    'referer': 'https://www.instagram.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

# while(True):
#
#     divs = driver.find_elements_by_class_name('v1Nh3')  # 这里最好使用xxxx_by_class_name，我尝试过用xpath绝对路径，但是好像对于页面变化比较敏感
#
#     for u in divs:
#         url_set.add(u.find_element_by_tag_name('a').get_attribute('href'))
#
#     if len(url_set) == url_set_size:  # 如果本次页面更新没有加入新的URL则可视为到达页面底端，跳出
#         break
#
#     url_set_size = len(url_set)
#
#     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()  # 三次滑动，保证页面更新足够
#     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
#     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
#
#     time.sleep(3)


# 下载图片：
def pic_download(u_download):
    global pic_index

    rec = requests.get(u_download, headers=header)

    selector = etree.HTML(rec.content)

    meta = selector.xpath('/html/head/meta[10]')[0]  # 使用xpath解析页面

    real_pic_url = meta.get("content").strip()

    pic_extend = real_pic_url[-4:]

    file_name = save_dir + "mirei_" + str(pic_index) + pic_extend

    pic_index += 1

    f = open(file_name, 'wb')

    pic_bin = requests.get(real_pic_url).content

    f.write(pic_bin)

    f.close()


# for url_ in url_set:
#     pic_download(url_)


if __name__ == '__main__':

    t = 0

    while (True):

        print '============== 1'

        divs = driver.find_elements_by_class_name('v1Nh3')  # 这里最好使用xxxx_by_class_name，我尝试过用xpath绝对路径，但是好像对于页面变化比较敏感

        for u in divs:
            url_set.add(u.find_element_by_tag_name('a').get_attribute('href'))

        print '============== 2'

        if len(url_set) == url_set_size:  # 如果本次页面更新没有加入新的URL则可视为到达页面底端，跳出
            print '本次页面更新没有加入新的URL则可视为到达页面底端，跳出'
            break

        url_set_size = len(url_set)

        print '============== 3'

        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()  # 三次滑动，保证页面更新足够
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

        time.sleep(3)

        print '============== 4'

        t = t + 1
        print '第%s次' % t
        if t == 2:
            break

    for url_ in url_set:
        print url_
        # pic_download(url_)

    print "下载结束"
