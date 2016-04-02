# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

def get_mongo_conn():
    return pymongo.MongoClient()

class CosstoresScrapyPipeline(object):
    def process_item(self, item, spider):
        _item = dict(item)
        #  db = get_mongo_conn().crawler
        #  db.test.insert(_item)
        return item
