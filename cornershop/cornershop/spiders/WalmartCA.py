# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy_splash import SplashRequest
from cornershop.items import CornershopItem


class WalmartcaSpider(scrapy.Spider):
    name = 'WalmartCA'
    allowed_domains = ['walmart.ca']
    start_urls = ['https://www.walmart.ca/sitemap-categories-en1.xml']

    def parse(self, response):
        # Remove namespace in order to work with XML files
        response.selector.remove_namespaces()
        urls = list(set(['/'.join(url.split('/')[:7]) for url in response.css('loc ::text').getall() if url.split('/')[4] == 'grocery' and len(url.split('/')) == 7]))[1:]
        for url in urls:
            yield SplashRequest(url, self.parse_category, args={'wait': 1})
    
    def parse_category(self, response):
        urls = response.css('article div.thumb-inner-wrap a::attr(href)').getall()
        for url in urls:
            yield response.follow(f'https://www.{self.allowed_domains[0]}{url}', self.parse_product)

        next_url = response.css('div.page-select-list-container a#loadmore::attr(href)').getall()
        if next_url:
            yield SplashRequest(f'https://www.{self.allowed_domains[0]}{next_url[0]}', self.parse_category, args={'wait': 1})

    def parse_product(self, response):
        product_info = response.css('div script ::text').getall()
        json_block = json.loads(product_info[0])
        json_block_two = json.loads(product_info[1])

        bar_code = response.css('script ::text').re_first(r'"upc":*(\[.*?\])\s*').split('"')[1]
        sku = json_block['sku']
        brand = json_block['brand']['name']
        name = json_block['name']
        description = json_block['description']
        package = response.css('p[data-automation*=short-description] ::text').get()
        image_urls = ",".join(json_block['image'])
        category = "|".join([element['item']['name'] for element in json_block_two['itemListElement']][1:-1])
        product_url = json_block_two['itemListElement'][-1]['item']['@id']

        product = CornershopItem(bar_code=bar_code, sku=sku, brand=brand, name=name, description=description, \
            package=package, image_urls=image_urls, category=category, product_url=product_url)
        yield product
