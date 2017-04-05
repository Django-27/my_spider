# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from .items import DangdangItem


class DangdangPipeline(object):

    def __init__(self):

        client = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                     port=settings['MONGODB_PORT'])
        tdb = client[settings['MONGODB_DBNAME']]

        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        if isinstance(item, DangdangItem):
            try:
                self.post.insert(dict(item))
            except Exception as e:
                pass

        return item
