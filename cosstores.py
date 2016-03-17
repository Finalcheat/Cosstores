#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Finalcheat'

import requests
import re
import datetime
from pyquery import PyQuery as pyq


class CosstoresGoodsListPrase(object):
    '''
    cosstores商品列表页解析
    such as : http://www.cosstores.com/gb/Women/Denim
    '''

    COSSTORES_HOST = 'http://www.cosstores.com'

    def __init__(self):
        # 列表页商品信息保存在该变量中
        self.goods_list = []

    def parse(self, url):
        # 解析第一页商品列表
        res = requests.get(url)
        assert res.status_code == 200
        jq = pyq(res.content)

        goods_list = jq('.list-container>ul>li>a')
        for r in goods_list:
            goods_url = r.get('href')
            if not goods_url:
                continue
            goods_url = '%s%s' % (CosstoresGoodsListPrase.COSSTORES_HOST, goods_url)
            goods_name = r.get('title')
            #  print goods_url, goods_name

            goods_item = {
                'url' : goods_url,
                'name' : goods_name,
            }
            self.goods_list.append(goods_item)

        # 解析ajax动态请求的商品列表页，第2-n页
        next_page = jq('#infiload_nav>a')
        if next_page:
            next_page = next_page[0]
            max_page = int(next_page.get('data-maxpage'))
            next_url = next_page.get('href')
            np = re.findall('page=(\d+)', next_url)
            if not np:
                return
            np = int(np[0])
            while np <= max_page:
                next_url = re.sub('page=(\d+)', 'page=%s' % (np), next_url)
                np += 1
                res = requests.get('%s%s' % (CosstoresGoodsListPrase.COSSTORES_HOST, next_url))
                assert res.status_code == 200
                jq_page = pyq(res.content)
                goods_list = jq_page('li>a')
                if not goods_list:
                    # 解析完了
                    break
                for r in goods_list:
                    goods_url = r.get('href')
                    if not goods_url:
                        continue
                    goods_url = '%s%s' % (CosstoresGoodsListPrase.COSSTORES_HOST, goods_url)
                    goods_name = r.get('title')
                    goods_item = {
                        'url' : goods_url,
                        'name' : goods_name,
                    }
                    self.goods_list.append(goods_item)


class CosstoresGoodsPrase(object):
    '''
    cosstores商品解析
    such as : http://www.cosstores.com/gb/Women/Knitwear/Silk_skirt_dress/46889-38392745.1#c-24479
    '''

    COSSTORES_HOST = 'http://www.cosstores.com'

    def __init__(self):
        # 商品id
        self.goods_id = ''
        # 商品类目id
        self.category_id = ''
        # 商品url链接
        self.url = ''
        # 商品名称
        self.name = ''
        # 商品原价
        self.original_price = ''
        # 商品当前价
        self.price = ''
        # 商品详细描述信息
        self.details = ''
        # 商品属性
        self.attributes = []
        # 商品货号
        self.code = ''
        # 商品颜色
        self.color = []
        # 商品图片
        self.image = []
        # 操作更新时间
        self.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    def parse(self, url):
        res = requests.get(url)
        assert res.status_code == 200
        jq = pyq(res.content)
        self.url = url
        self.price = jq('.PriceContainer').text()
        self.color = jq('.colorLabel').text()
        self.name = jq('.productInfo>h1').text()
        category_id = re.findall('/(\d+)-', url)
        self.category_id = category_id[0] if category_id else ''
        images = jq('.productSlideshow>ul>li>div>img')
        image_list = []
        for r in images:
            image_url = r.get('src')
            if not image_url:
                continue
            image_list.append('%s%s' % (CosstoresGoodsPrase.COSSTORES_HOST, image_url))
        self.image = image_list
        first_image = image_list[0] if image_list else ''
        goods_id = re.findall('/(\d+)/', first_image)
        self.goods_id = str(goods_id[0]) if goods_id else ''

        # ajax动态请求
        goods_detail_ids = jq('.productSizes>label>input')
        goods_detail_id = goods_detail_ids[0].get('value') if goods_detail_ids else ''
        if goods_detail_id:
            goods_detail_url = 'http://www.cosstores.com/gb/product/GetVariantData?variantId=%s&lookID=null&image=0' % (goods_detail_id)
            res = requests.get(goods_detail_url)
            assert res.status_code == 200
            result = res.json()
            self.code = result.get('HMOrderNo', '')
            self.original_price = result.get('DefaultPriceWithCurrency', '')
            self.price = result.get('PriceWithCurrency', '')
            self.attributes = result.get('Attributes', [])
            self.details = result.get('DescriptionShort', '')


if __name__ == '__main__':
    # goods list
    url = 'http://www.cosstores.com/gb/Women/Coats_Jackets'
    cosListObj = CosstoresGoodsListPrase()
    cosListObj.parse(url)
    print cosListObj.__dict__

    # goods detail
    goods_url = 'http://www.cosstores.com/gb/Women/Knitwear/Silk_skirt_dress/46889-38392745.1#38392750'
    cosGoodsObj = CosstoresGoodsPrase()
    cosGoodsObj.parse(goods_url)
    for k, v in cosGoodsObj.__dict__.items():
        print k, v
