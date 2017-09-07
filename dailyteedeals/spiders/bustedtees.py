# -*- coding: utf-8 -*-
import random
import scrapy
import urlparse
from dailyteedeals.items import ProductItemLoader


class BustedteesCommon(scrapy.Spider):
    allowed_domains = ["bustedtees.com"]

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('description', '//div[@id="description"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//div[@class="gallery-image"]/img[contains(@src, ".gif")]/@src')
        loader.add_xpath('artist_name', '//div[@id="description"]/text()', re=r'Design by (.+?)\.?\s*$')
        loader.add_value('artist_name', 'BustedTees')
        loader.add_xpath('prices', '//span[@id="sale_price"]/text()')
        loader.add_xpath('prices', '//span[@class="price"]/text()')

        tags = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        loader.add_value('tags', tags.split(','))

        yield loader.load_item()


class BustedteesDealSpider(BustedteesCommon):
    name = "bustedtees_deal"
    start_urls = ['http://www.bustedtees.com/clearance/all-categories/all-colors/all-styles/all-sizes/1/512']

    def parse(self, response):
        products = response.xpath('//div[@class="thumbnail"]/a/@href').extract()
        random.shuffle(products)
        products.insert(0, "/mysterytee")
            
        for product_url in products[:10]:
            yield scrapy.Request(urlparse.urljoin(response.url, product_url), callback=self.parse_product_page)

            


class BustedteesFullSpider(BustedteesCommon):
    name = "bustedtees_full"
    start_urls = [
        'http://www.bustedtees.com/tshirts/all-categories/all-colors/all-styles/all-sizes/1/512']

    def parse(self, response):
        for product_url in response.xpath('//a[@id="tile_product"]/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url), callback=self.parse_product_page)
