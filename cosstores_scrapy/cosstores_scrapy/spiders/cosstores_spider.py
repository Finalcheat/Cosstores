#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import requests
import re
from cosstores_scrapy.items import CosstoresScrapyItem


class CosstoresSpider(scrapy.Spider):
    '''
    Cosstores
    '''

    name = 'cosstores'
    allowed_domains = ["cosstores.com"]
    start_urls = [
        'http://www.cosstores.com/gb/Women/Coats_Jackets',
    ]
    HOST = 'http://www.cosstores.com'

    def parse(self, response):
        #  url = response.url
        goods_list = response.xpath('//section[@class="list-container"]/ul/li/a')
        for g in goods_list:
            goods_url = g.xpath('@href').extract()
            if not goods_url:
                continue
            goods_url = '{}{}'.format(self.HOST, goods_url[0])
            yield scrapy.Request(goods_url, callback = self.parse_goods)

    def parse_goods(self, response):
        item = CosstoresScrapyItem()

        url = response.url

        item['url'] = url

        category_id = re.findall('/(\d+)-', url)
        item['category_id'] = category_id[0] if category_id else ''

        name = response.xpath('//div[@class="productInfo"]/h1/text()').extract()
        item['name'] = name[0] if name else ''

        images = response.xpath('//div[contains(@class, "productSlideshow")]/ul/li/div/img')
        _image = []
        for r in images:
            _image.append('{}{}'.format(self.HOST, r.xpath("@src").extract()[0]))
        item['image'] = _image

        first_image = _image[0] if _image else ''
        goods_id = re.findall('/(\d+)/', first_image)
        item['goods_id'] = str(goods_id[0]) if goods_id else ''

        # ajax动态请求
        goods_detail_id = response.xpath('//div[@class="productSizes"]/label/input')
        goods_detail_id = goods_detail_id[0] if goods_detail_id else ''
        goods_detail_id = goods_detail_id.xpath("@value").extract()[0] if goods_detail_id else ''
        #  print goods_detail_id
        if goods_detail_id:
            goods_detail_url = '{}//product/GetVariantData?variantId={}&lookID=null&image=0'.format(self.HOST, goods_detail_id)
            res = requests.get(goods_detail_url)
            assert res.status_code == 200
            result = res.json()
            item['code'] = result.get('HMOrderNo', '')
            item['original_price'] = result.get('DefaultPriceWithCurrency', '')
            item['price'] = result.get('PriceWithCurrency', '')
            item['attributes'] = result.get('Attributes', [])
            item['details'] = result.get('DescriptionShort', '')

        yield item
