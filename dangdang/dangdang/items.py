# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DangdangItem(Item):

    category_big_name = Field()
    category_small_name = Field()
    book_author = Field()
    book_price_cn = Field()
    book_name = Field()
