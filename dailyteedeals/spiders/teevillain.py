# -*- coding: utf-8 -*-
import re
import urlparse
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class TeevillainSpider(scrapy.Spider):
    name = "teevillain_deal"
    allowed_domains = ["teevillain.com"]
    start_urls = ['https://www.teevillain.com']

    def parse(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//img[@class="product_image"]/@alt')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//section[contains(@class, "teeDesign")]//img/@src')
        loader.add_xpath('artist_name', '//a[contains(@href, "designer")][1]/text()')
        loader.add_xpath('prices', '//span[contains(@class, "currentprice")]/text()')

        artist_url = response.xpath('//a[contains(@href, "designer")][1]/@href').extract_first()
        request = scrapy.Request(artist_url, callback=self.__parse_artist_page, dont_filter=True)
        request.meta['item'] = loader.load_item()
        yield request

    def __parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_urls', '//div[@class="profileInfo left"]//a/@href')
        return loader.load_item()
