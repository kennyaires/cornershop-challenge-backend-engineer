import scrapy


class CornershopItem(scrapy.Item):
    bar_code = scrapy.Field()
    sku = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    package = scrapy.Field()
    image_urls = scrapy.Field()
    category = scrapy.Field()
    product_url = scrapy.Field()
