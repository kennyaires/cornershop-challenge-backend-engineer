# -*- coding: utf-8 -*-
import scrapy


class WalmartcaSpider(scrapy.Spider):
    name = 'WalmartCA'
    allowed_domains = ['walmart.ca']
    start_urls = ['http://walmart.ca/']

    def parse(self, response):
        pass
