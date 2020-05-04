# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CornershopItem(scrapy.Item):
    # define the fields for your item here like:
    bar_code = scrapy.Field()
    sku = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    package = scrapy.Field()
    image_urls = scrapy.Field()
    category = scrapy.Field()
    product_url = scrapy.Field()
