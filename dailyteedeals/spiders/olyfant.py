# -*- coding: utf-8 -*-
import urlparse
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class OlyfantSpider(scrapy.Spider):
    name = "olyfant_full"
    allowed_domains = ["olyfant.com"]
    start_urls = ['https://olyfant.com/shop']

    def parse(self, response):
        for sel in response.css('.shirt a'):
            product_url = sel.xpath('@href').extract_first()
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//span[@class="productname"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//meta[@property="og:image"]/@content')
        loader.add_value('artist_name', response.xpath('//meta[@property="og:title"]/@content').extract_first().rsplit(' by ', 1)[1])
        loader.add_xpath('prices', '(//div[@class="productdt"]//span/text())[last()]')
        return loader.load_item()
