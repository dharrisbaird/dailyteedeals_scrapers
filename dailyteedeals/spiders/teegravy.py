# -*- coding: utf-8 -*-
import scrapy
from dailyteedeals.items import ProductItemLoader


class TeegravySpider(scrapy.Spider):
    name = "teegravy_deal"
    allowed_domains = ["teegravy.com"]
    start_urls = ['http://www.teegravy.com']

    def parse(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//div[@id="shirt-name"]/h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//div[@id="design-large"]/a/@href')
        loader.add_value('artist_name', 'Tee Gravy')
        loader.add_value('artist_urls', ['http://www.teegravy.com'])
        loader.add_xpath('prices', '//p[@class="shirt-dollars"]/text()')
        return loader.load_item()
