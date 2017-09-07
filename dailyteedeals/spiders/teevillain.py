# -*- coding: utf-8 -*-
import re
import urlparse
import scrapy
from dailyteedeals.items import ProductItemLoader


class TeevillainSpider(scrapy.Spider):
    name = "teevillain_deal"
    allowed_domains = ["teevillain.com"]
    start_urls = ['https://www.teevillain.com']

    def parse(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//span[@class="product-name"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//div[@class="showcase-image"]/img/@src')
        loader.add_xpath('artist_name', '//span[@class="product-artist"]/a/text()')
        loader.add_value('prices', '$10')
        return loader.load_item()
