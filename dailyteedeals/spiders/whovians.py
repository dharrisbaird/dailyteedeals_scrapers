# -*- coding: utf-8 -*-
import scrapy
import urlparse
from dailyteedeals.items import ProductItemLoader


class WhoviansSpider(scrapy.Spider):
    name = "whovians_full"
    allowed_domains = ["whovians.com"]
    start_urls = ['http://whovians.com/shop/shirts/']

    def parse(self, response):
        for product_url in response.xpath('//div[@class="product-item"]/a/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('artist_name', '//span[text()="Artist:"]/following::a[1]/text()')
        loader.add_xpath('artist_urls', '//span[text()="Artist:"]/following::a[1]/@href')
        loader.add_xpath('image_url', '//meta[@property="og:image"]/@content')
        loader.add_xpath('prices', '//span[@class="price-new"]/text()')
        return loader.load_item()
