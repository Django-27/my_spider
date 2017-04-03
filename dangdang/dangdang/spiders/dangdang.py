# -*= coding=utf-8 -*-
"""
scrapy startproject name是最好是在虚拟环境中进行
否则有些怪异错误，使用scrapy_3env环境
"""
import random
import scrapy
from scrapy import Selector
from ..items import DangdangItem
# from scrapy_redis.spiders import RedisSpider

class DangdangSpider():
    name = 'dangdangspider'
    redis_key = 'dangdangspider:urls'
    allowed_domains = ['dangdang.com']
    start_urls = 'http://category.dangdang.com/cp01.00.00.00.00.00.html'

    def start_requests(self):
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': ua}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)
    """
    感觉有点乱，scrapy-redis一般是用来做分布式的，这里我感觉直接用Spider类就满足需求了。还有那个lxml的库完全可以不用，scrapy已经帮你封装好了，直接用response.xpath()就可以了。
    嗯，是的 scrapy-redis 主要用它去重一下链接。lxml库可以不用的
    """
    def parse(self, response):
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': ua}
        lists = response.body.decode('gbk')
        selector = response.HTML(lists)
        goodslist = selector.xpath('//*[@id="leftCate"]/ul/li')
        for goods in goodslist:
            try:
                category_big = goods.xpath('a/text()').pop().replace('   ', '')  # 大种类
                category_big_id = goods.xpath('a/@href').pop().split('.')[1]  # id
                category_big_url = "http://category.dangdang.com/pg1-cp01.{}.00.00.00.00.html". \
                    format(str(category_big_id))
                # print("{}:{}".format(category_big_url,category_big))
                yield scrapy.Request(url=category_big_url, headers=headers, callback=self.detail_parse,
                                     meta={"ID1": category_big_id, "ID2": category_big})
            except Exception:
                pass

    def detail_parse(self, response):
        '''
        ID1:大种类ID   ID2:大种类名称   ID3:小种类ID  ID4:小种类名称
        '''
        url = 'http://category.dangdang.com/pg1-cp01.{}.00.00.00.00.html'.format(response.meta["ID1"])
        category_small = requests.get(url)
        contents = etree.HTML(category_small.content.decode('gbk'))
        goodslist = contents.xpath('//*[@class="sort_box"]/ul/li[1]/div/span')
        for goods in goodslist:
            try:
                category_small_name = goods.xpath('a/text()').pop().replace(" ", "").split('(')[0]
                category_small_id = goods.xpath('a/@href').pop().split('.')[2]
                category_small_url = "http://category.dangdang.com/pg1-cp01.{}.{}.00.00.00.html". \
                    format(str(response.meta["ID1"]), str(category_small_id))
                yield scrapy.Request(url=category_small_url, callback=self.third_parse,
                                     meta={"ID1": response.meta["ID1"], \
                                           "ID2": response.meta["ID2"], "ID3": category_small_id,
                                           "ID4": category_small_name})
                # print("============================ {}".format(response.meta["ID2"]))  # 大种类名称
                # print(goods.xpath('a/text()').pop().replace(" ","").split('(')[0])   # 小种类名称
                # print(goods.xpath('a/@href').pop().split('.')[2])   # 小种类ID
            except Exception:
                pass
    def third_parse(self, response):
        for i in range(1, 101):
            url = 'http://category.dangdang.com/pg{}-cp01.{}.{}.00.00.00.html'.format(str(i),
                                                                                      response.meta["ID1"], \
                                                                                      response.meta["ID3"])
            try:
                contents = requests.get(url)
                contents = etree.HTML(contents.content.decode('gbk'))
                goodslist = contents.xpath('//*[@class="list_aa listimg"]/li')
                for goods in goodslist:
                    item = DangdangItem()
                    try:
                        item['comments'] = goods.xpath('div/p[2]/a/text()').pop()
                        item['title'] = goods.xpath('div/p[1]/a/text()').pop()
                        item['time'] = goods.xpath('div/div/p[2]/text()').pop().replace("/", "")
                        item['price'] = goods.xpath('div/p[6]/span[1]/text()').pop()
                        item['discount'] = goods.xpath('div/p[6]/span[3]/text()').pop()
                        item['category1'] = response.meta["ID4"]  # 种类(小)
                        item['category2'] = response.meta["ID2"]  # 种类(大)
                    except Exception:
                        pass
                    yield item
            except Exception:
                pass

def ip_pool(num):  # 返回的有效ip个数
    ip_list = []
    with open('./../../../host_ip.txt', 'r') as f:
        ips = f.readlines()
    for i in range(num):
            ip_list.append('http://' + ips[i].strip('\n'))
    return ip_list

if __name__ == '__main__':
    ps = ip_pool(5)
    print(random.choice(ps))
