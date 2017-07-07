# -*- coding: utf-8 -*-
import scrapy
import urlparse
from dailyteedeals.items import ProductItemLoader


class Teeminus24Common(scrapy.Spider):
    allowed_domains = ["teeminus24.com"]

    def parse(self, response):
        for product_url in response.xpath('//div[contains(@class, "products")]//a/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_value('artist_name', 'teeminus24')
        loader.add_value('artist_urls', ['http://teeminus24.com'])
        loader.add_xpath('prices', '//span[@id="listPrice"]/text()')
        loader.add_value('image_url', response.body, re=r'"fullsize":{"url":"(.*?)"')
        return loader.load_item()

class Teeminus24DealSpider(Teeminus24Common):
    name = "teeminus24_deal"
    start_urls = ['http://shop.teeminus24.com/Shirt-of-the-Week_c3.htm']

class Teeminus24FullSpider(Teeminus24Common):
    name = "teeminus24_full"
    start_urls = ['http://shop.teeminus24.com/Home_c1.htm?page=all']
