# -*- coding=utf-8 -*-
import requests
from lxml import html
import urllib
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Upgrade-Insecure-Requests': '1'
}
session = requests.Session()
s = session.get('http://www.taobao.com/', headers=headers)
s = session.get('https://www.taobao.com/')
print(s.status_code)

s = session.get('https://s.taobao.com/search?q=%E6%95%A3%E8%A3%85%E8%8D%9E%E9%BA%A6%E5%A3%B3&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170408')
# '%E6%95%A3%E8%A3%85%E8%8D%9E%E9%BA%A6%E5%A3%B3&' 散装荞麦壳


open('tmp.html', 'w', encoding='utf-8').write(s.text)

# dom = html.fromstring(s.content)

# lists = dom.xpath('//div[@class="grid g-clearfix"]/div/div')
# print(len(lists))



# &imgfile=
#
# &commend=
#
# all&ssid=s5-e&search_type=item
#
# &sourceId=tb.index
#
# &spm=a21bo.50862.201856-taobao-item.1
#
# &ie=utf8&initiative_id=tbindexz_20170408
