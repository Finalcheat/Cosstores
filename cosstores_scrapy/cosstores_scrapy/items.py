# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CosstoresScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    # 商品id
    goods_id = scrapy.Field()
    # 商品类目id
    category_id = scrapy.Field()
    # 商品url链接
    url = scrapy.Field()
    # 商品名称
    name = scrapy.Field()
    # 商品描述
    details = scrapy.Field()
    # 商品原价
    original_price = scrapy.Field()
    # 商品当前价
    price = scrapy.Field()
    # 商品详细描述信息
    detail = scrapy.Field()
    # 商品属性
    attributes = scrapy.Field()
    # 商品货号
    code = scrapy.Field()
    # 商品颜色
    color = scrapy.Field()
    # 商品图片
    image = scrapy.Field()
    # 操作更新时间
