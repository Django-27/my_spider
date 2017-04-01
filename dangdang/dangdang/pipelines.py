# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from .items import DangdangItem

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting


class DangdangPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db_name]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item):
        if isinstance(item, DangdangItem):
            try:
                book_info = dict(item)
                if self.post.insert(book_info):
                    pass
            except Exception as e:
                pass

        return item
