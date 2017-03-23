# encoding=utf-8
import requests
from lxml import html
import urllib

DOWNLOAD_URL = 'http://movie.douban.com/top250/'

headers = {
    'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0;\
     Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)'
}

next_page = DOWNLOAD_URL
while next_page:
    r = requests.get(next_page)
    dom = html.fromstring(r.content)
    moves = dom.xpath('//ol/li')
    for move in moves:
        num = move.xpath('.//div/em/text()')[0]

        name_cn = move.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0]
        name_en = move.xpath('./div/div[2]/div[1]/a/span[2]/text()')[0].strip()[2:]

        rating_num = move.xpath('.//span[@class="rating_num"]/text()')[0]
        comment_num = move.xpath('.//div[@class="star"]/span[4]/text()')[0]

        quote = move.xpath('.//p[@class="quote"]/span/text()')  # 有可能为空
        if quote:
            quote = quote[0]
        else:
            quote = "短评：无"

        img = move.xpath('.//a/img/@src')[0]
        # urllib.request.urlretrieve(url=img, filename='%s.jpg'.format(name_cn))  # 下载图片65*100

        print(num, name_cn, name_en, rating_num, comment_num, quote, img)

    if dom.xpath('.//span[@class="next"]/a'):
        next_page = DOWNLOAD_URL + dom.xpath('.//span[@class="next"]/a/@href')[0]
    else:
        next_page = ''

    break


