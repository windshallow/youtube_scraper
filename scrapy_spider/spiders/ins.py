# -*- coding: utf-8 -*-
"""
Authored by: LRW
"""
import requests
import time
import os
import json
import sys
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def resource_download(u_download):
    print("Now downloading:" + u_download)

    global pic_index
    rec = requests.get(u_download, headers=header)

    selector = etree.HTML(rec.content)

    script = selector.xpath('/html/body/script[1]')[0]  # 获得页面js脚本，用于分析页面资源情况

    scr_json = script.text[21:-1]
    try:
        json_res = json.loads(scr_json)  # 获得相应页面json信息
    except:
        print("Get page resource failed,can't convert to json! Failed URL:" + u_download)
        sys.exit()

    media_info = json_res['entry_data']["PostPage"][0]["graphql"]["shortcode_media"]

    if media_info["__typename"] == "GraphImage":
        download_single_pic(media_info)

    elif media_info["__typename"] == "GraphSidecar":
        download_multi_media(media_info)

    elif media_info["__typename"] == "GraphVideo":
        download_single_video(media_info)


def download_single_pic(media_info, filename=None):
    pic_url = media_info['display_url'].strip()

    ext = pic_url.split('.')[-1]

    if filename == None:

        timestamp = media_info['taken_at_timestamp']

        localtime = time.localtime(timestamp)

        pic_name = save_dir + 'mirei_' + time.strftime("%Y-%m-%d_%H%M%S", localtime) + '.' + ext

    else:

        pic_name = filename

    f = open(pic_name, 'wb')

    pic_bin = requests.get(pic_url).content

    f.write(pic_bin)

    f.close()


def download_multi_media(media_info):
    # download_single_pic(media_info)

    pics_url = media_info['edge_sidecar_to_children']['edges']

    pic_count = len(pics_url)

    timestamp = media_info['taken_at_timestamp']

    localtime = time.localtime(timestamp)

    for i in range(pic_count):

        node = pics_url[i]['node']

        if node['__typename'] == 'GraphImage':

            pic_url = node['display_url'].strip()

            ext = pic_url.split('.')[-1]

            pic_name = save_dir + 'mirei_' + time.strftime("%Y-%m-%d_%H%M%S", localtime) + '_' + str(i) + '.' + ext

            download_single_pic(node, pic_name)

        elif node['__typename'] == 'GraphVideo':

            video_url = node['video_url'].strip()

            ext = video_url.split('.')[-1]

            video_name = save_dir + 'mirei_' + time.strftime("%Y-%m-%d_%H%M%S", localtime) + '_' + str(i) + '.' + ext

            download_single_video(node, video_name)

        else:
            pass


def download_single_video(media_info, filename=None):
    video_url = media_info['video_url'].strip()

    ext = video_url.split('.')[-1]

    if filename == None:

        timestamp = media_info['taken_at_timestamp']

        localtime = time.localtime(timestamp)

        video_name = save_dir + 'mirei_' + time.strftime("%Y-%m-%d_%H%M%S", localtime) + '.' + ext

    else:

        video_name = filename

    f = open(video_name, 'wb')

    video_bin = requests.get(video_url).content

    f.write(video_bin)

    f.close()


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    driver = webdriver.Chrome(chrome_options=options)

    # target = "https://www.instagram.com/mirei_kiritani_/"
    # target = 'https://www.instagram.com/kasumi_arimura.official/'
    target = 'https://www.instagram.com/mirei.kiritani/'

    url_set = set([])

    driver.get(target)

    url_set_size = 0

    # save_dir = './pic_test/'
    save_dir = '/Users/admin/Desktop/html'

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    header = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        'cookie': 'shbid=4419; rur=PRN; mcd=3; mid=W1E7cAALAAES6GY5Dyuvmzfbywic; csrftoken=uVspLzRYlxjToqSoTlf09JVaA9thPkD0; urlgen="{\"time\": 1532050288\054 \"2001:da8:e000:1618:e4b8:8a3d:8932:2621\": 23910\054 \"2001:da8:e000:1618:6c15:ccda:34b8:5dc8\": 23910}:1fgVTv:SfLAhpEZmvEcJn0037FXFMLJr0Y"',
        'referer': 'https://www.instagram.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    while (True):

        divs = driver.find_elements_by_class_name('v1Nh3')

        for u in divs:
            real_url = u.find_element_by_tag_name('a').get_attribute('href')
            url_set.add(real_url)

        print("Number of urls is now:" + str(url_set_size))

        if len(url_set) == url_set_size or len(url_set) > 30:
            break

        url_set_size = len(url_set)

        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        # driver.implicitly_wait(30) #智能等待30秒

    url_set_size = len(url_set)

    print("Starting download............")
    for ind, url_ in enumerate(url_set):
        # pic_download(url_)
        # resource_download(url_)
        print(url_ + ' has been downloaded, and the total process finished {:.2f}%'.format(ind / url_set_size * 100))