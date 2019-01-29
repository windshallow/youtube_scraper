# -*- coding: utf-8 -*-

import json

f = open('/Users/admin/Desktop/funny/youtube_scraper/local_resources/mobile_user_agent.json', 'r')
MUA_LIST = [i.get('user_agent') for i in json.load(f)]
f.close()


if __name__ == '__main__':
    print MUA_LIST
    print MUA_LIST[0]
