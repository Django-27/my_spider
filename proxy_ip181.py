# -*- coding=utf-8 -*-
import requests
from lxml import html as HTML


headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.ip181.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

r = requests.get('http://www.ip181.com/', headers=headers)
dom = HTML.fromstring(r.content)

for info in dom.xpath('//tbody/tr'):
    ip = info.xpath('./td[1]/text()')
    port = info.xpath('./td[2]/text()')

    print('ip181', ip, port)

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'list.proxylistplus.com',
            'If-Modified-Since': 'Mon, 20 Feb 2017 07:47:35 GMT',
            'If-None-Match': 'list381487576865',
            'Referer': 'https://list.proxylistplus.com/Fresh-HTTP-Proxy',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
        }

for page_num in range(5):
    url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(page_num+1)
    r = requests.get(url=url, headers=headers)
    dom = HTML.fromstring(r.content)

    for i, info in enumerate(dom.xpath('//table[@class="bg"]/tr')):
        ip = info.xpath('./td[2]/text()')
        port = info.xpath('./td[3]/text()')

        print('proxylistplus', page_num+1, i, ip, port)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'm.66ip.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

for page_num in range(10):
    url = 'http://m.66ip.cn/{}.html'.format(page_num+1)
    r = requests.get(url=url, headers=headers)
    dom = HTML.fromstring(r.content)

    for i, info in enumerate(dom.xpath('//table/tr')):
        ip = info.xpath('./td[1]/text()')
        port = info.xpath('./td[2]/text()')

        print('66ip', page_num+1, i, ip, port)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.xicidaili.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

r = requests.get('http://www.xicidaili.com/', headers=headers)
dom = HTML.fromstring(r.content)

for info in dom.xpath('//table/tr'):
    ip = info.xpath('./td[2]/text()')
    port = info.xpath('./td[3]/text()')

    print('西刺代理 ', ip, port)

