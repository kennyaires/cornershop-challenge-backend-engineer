# -*- coding: utf-8 -*-
import scrapy
import json

from cornershop.items import CornershopItem
from references import ALLOWED_CATEGORIES


class WalmartcaSpider(scrapy.Spider):
    name = 'WalmartCA'
    allowed_domains = ['walmart.ca']
    start_urls = [f'https://www.walmart.ca/sitemap-product{n}-en.xml/' for n in range(100, 101)]

    def parse(self, response):
        # Remove namespace in order to work with XML files
        response.selector.remove_namespaces()
        for url in response.css('loc ::text').getall():
            yield response.follow(url, self.parse_product)

    def parse_product(self, response):

        product_info = response.css('div script ::text').getall()
        json_block = json.loads(product_info[0])
        json_block_two = json.loads(product_info[1])
        category = [element['item']['name'] for element in json_block_two['itemListElement']][1:-1]

        # if not category[0].strip() in ALLOWED_CATEGORIES:
        #     return
        print(category[0].strip() in ALLOWED_CATEGORIES)

        bar_code = response.css('script ::text').re_first(r'"upc":*(\[.*?\])\s*').split('"')[1]
        sku = json_block['sku']
        brand = json_block['brand']['name']
        name = json_block['name']
        description = json_block['description']
        package = response.css('p[data-automation*=short-description] ::text').get()
        image_urls = ",".join(json_block['image'])
        category = "|".join(category)
        product_url = json_block_two['itemListElement'][-1]['item']['@id']

        product = CornershopItem(bar_code=bar_code, sku=sku, brand=brand, name=name, description=description, \
            package=package, image_urls=image_urls, category=category, product_url=product_url)
        yield product
