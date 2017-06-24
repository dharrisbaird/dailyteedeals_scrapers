# -*- coding: utf-8 -*-
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class AngloteesSpider(scrapy.Spider):
    name = "anglotees_deal"
    allowed_domains = ["anglotees.com"]
    start_urls = ['https://anglotees.com']

    def parse(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//div[contains(@class, "wpb_single_image")]/h2/text()')
        loader.add_xpath('url', '//div[contains(@class, "wpb_single_image")]//a/@href')
        loader.add_xpath('image_url', '//div[contains(@class, "wpb_single_image")]//img/@src')
        loader.add_value('artist_name', 'Anglotees')
        loader.add_value('artist_urls', ['http://anglotees.com/'])
        loader.add_value('prices', '$22.99')
        return loader.load_item()
