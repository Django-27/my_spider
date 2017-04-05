# -*= coding=utf-8 -*-
import random
import scrapy
from scrapy import Selector
from ..items import DangdangItem
from lxml import html
# from scrapy_redis.spiders import RedisSpider


class DangdangSpider(scrapy.Spider):
    name = 'dangdangspider'

    redis_key = 'dangdangspider:urls'
    allowed_domains = ['dangdang.com']
    start_urls = 'http://category.dangdang.com/cp01.00.00.00.00.00.html' # # 大种类, 共53个


    def start_requests(self):
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': ua}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': ua}
        goodslist = response.xpath('//div[@class="sort_box"]//ul/li').extract()
        for goods in goodslist:
            try:
                goods = html.fromstring(goods)
                category_big_name = goods.xpath('a/@title')[0]  # 大种类, 共53个
                category_big_url = goods.xpath('./a/@href')[0]
                yield scrapy.Request(url=response.urljoin(category_big_url),
                                     headers=headers, callback=self.detail_parse,
                                     meta={"category_big_name": category_big_name})
            except Exception:
                pass

    def detail_parse(self, response):
        '''
        http://category.dangdang.com/cp01.47.00.00.00.00.html#ddclick?act=clickcat&pos=0_0_0_p&cat=01.25.00.00.00.00&key=&qinfo=&pinfo=131429_1_60&minfo=&ninfo=&custid=&permid=&ref=&rcount=&type=&t=1491304>
        '''
        goodslist = response.xpath('//div[@class="link max"]/span').extract()
        for goods in goodslist:
            try:
                goods = html.fromstring(goods)
                category_small_name = goods.xpath('a/@title')[0]
                category_small_url = goods.xpath('a/@href')[0]   # 小种类，不确定
                yield scrapy.Request(url=response.urljoin(category_small_url),
                                     callback=self.third_parse,
                                     meta={"category_small_name": category_small_name,
                                           "category_big_name": response.meta['category_big_name']})
            except Exception:
                pass

    def third_parse(self, response):
        '''
        http://category.dangdang.com/cp01.47.02.00.00.00.html#ddclick?act=clickcat&pos=0_0_0_p&cat=01.47.00.00.00.00&key=&qinfo=&pinfo=1021302_1_60&minfo=&ninfo=&custid=&permid=&ref=&rcount=&type=&t=1491375720000&sell_run=0&searchapi_version=eb_split'
        '''
        item = DangdangItem()
        for _ in range(3):
            books = response.xpath('//div[@class="con shoplist"]/ul/li')  # 正常一页60项
            for book in books:
                book_price_cn = book.css('p.price span.price_n::text').extract_first()
                book_author = book.css('p.author a::text').extract_first()
                book_name = book.css('p.name a::text').extract_first()

                # print(response.meta['category_big_name'], response.meta['category_small_name'], book_author, book_price_cn, book_name)
                item['book_price_cn'] = book_price_cn
                item['book_name'] = book_name
                item['book_author'] = book_author
                item['category_big_name'] = response.meta['category_big_name']
                item['category_small_name'] = response.meta['category_small_name']
                yield item

            next_page = response.css('li.next a::attr(href)').extract_first()
            if next_page is not None:
                yield scrapy.Request(response.urljoin(next_page), callback=self.third_parse)




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