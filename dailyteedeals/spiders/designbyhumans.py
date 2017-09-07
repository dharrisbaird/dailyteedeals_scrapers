# -*- coding: utf-8 -*-
import re
import scrapy
import random
from dailyteedeals.items import ProductItemLoader


class DesignbyhumansCommon(scrapy.Spider):
    allowed_domains = ["designbyhumans.com"]

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)

        style = response.xpath(
            '//label[@class="color-label selected"]//span/@style').extract_first()

        artist_name = response.xpath('//span[@class="name"]/text()').extract_first()

        loader.add_xpath('name', '//h1[@id="product-title"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//meta[@property="og:image"]/@content')
        loader.add_xpath('prices', '//span[@id="product_price"]/text()')
        loader.add_value('artist_name', artist_name)
        loader.add_value('artist_urls', 'https://www.designbyhumans.com/shop/' + artist_name)
        return loader.load_item()


class DesignbyhumansDealSpider(DesignbyhumansCommon):
    name = "designbyhumans_deal"
    start_urls = ['https://www.designbyhumans.com/shop/pop-culture-mens-t-shirts/']

    def parse(self, response):
        product_urls = response.xpath('//a[contains(@class, "listing-trigger")]/@href').extract()
        random.shuffle(product_urls)
        for product_url in product_urls[:4]:
            yield scrapy.Request(product_url, callback=self.parse_product_page)


class DesignbyhumansFullSpider(DesignbyhumansCommon):
    name = "designbyhumans_full"

    URL_TEMPLATE = 'https://www.designbyhumans.com/shop/best-geek-mens-t-shirts/page/%d/'

    def start_requests(self):
        for page in range(1, 30):
            yield scrapy.Request(self.URL_TEMPLATE % page, callback=self.__parse_list_page)

    def __parse_list_page(self, response):
        for product_url in response.xpath('//a[contains(@class, "listing-trigger")]/@href').extract():
            yield scrapy.Request(product_url, callback=self.parse_product_page)
