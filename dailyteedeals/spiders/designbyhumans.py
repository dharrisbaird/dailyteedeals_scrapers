# -*- coding: utf-8 -*-
import re
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class DesignbyhumansCommon(scrapy.Spider):
    allowed_domains = ["designbyhumans.com"]

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)

        style = response.xpath(
            '//label[@class="color-label selected"]//span/@style').extract_first()
        color = re.match(r'background-color:#(.+)', style).group(1)
        image_url = response.xpath('//meta[@property="og:image"]/@content').extract_first()
        image_url = re.sub(r'[a-f0-9]{6}\.jpg$', color + '.jpg', image_url)
        image_url = re.sub(r'-\d+x\d+-', '-1200x1200-', image_url)

        artist_name = response.xpath('//span[@class="name"]/text()').extract_first()

        loader.add_xpath('name', '//h1[@id="product-title"]/text()')
        loader.add_value('url', response.url)
        loader.add_value('image_url', image_url)
        loader.add_xpath('prices', '//span[@id="product_price"]/text()')
        loader.add_value('artist_name', artist_name)
        loader.add_value('artist_urls', 'https://www.designbyhumans.com/shop/' + artist_name)
        return loader.load_item()


class DesignbyhumansDealSpider(DesignbyhumansCommon):
    name = "designbyhumans_deal"
    start_urls = ['https://www.designbyhumans.com/shirt-of-the-day/']

    def parse(self, response):
        return self.parse_product_page(response)


class DesignbyhumansFullSpider(DesignbyhumansCommon):
    name = "designbyhumans_full"

    URL_TEMPLATE = 'https://www.designbyhumans.com/shop/best-geek-mens-t-shirts/page/%d/'

    def start_requests(self):
        for page in range(1, 30):
            yield scrapy.Request(self.URL_TEMPLATE % page, callback=self.__parse_list_page)

    def __parse_list_page(self, response):
        for product_url in response.xpath('//a[contains(@class, "listing-trigger")]/@href').extract():
            yield scrapy.Request(product_url, callback=self.parse_product_page)
