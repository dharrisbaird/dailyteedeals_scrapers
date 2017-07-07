# -*- coding: utf-8 -*-
import urlparse
import scrapy
from dailyteedeals.items import ProductItemLoader


class SnorgteesCommon(scrapy.Spider):
    allowed_domains = ["www.snorgtees.com"]
    start_urls = ['http://www.snorgtees.com/t-shirts']

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('description', '//div[@class="short-description"]//p/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//a[contains(@class, "artwork-image")]/@href')
        loader.add_xpath('image_url', '//a[@class="artworkImage Guys default"]/@data-mask')
        loader.add_xpath('image_url', '//img[contains(@data-zoom-image, "fullpic")]/@data-zoom-image')
        loader.add_value('artist_name', 'SnorgTees')
        loader.add_value('artist_urls', ['https://twitter.com/snorgtees'])
        loader.add_xpath('prices', '//p[@class="special-price"]//span[@class="price"]/text()')
        loader.add_xpath('prices', '//span[@class="price"]/text()')
        return loader.load_item()


class SnorgteesDealSpider(SnorgteesCommon):
    name = "snorgtees_deal"

    def parse(self, response):

        for product_url in response.xpath('(//p[@class="special-price"]/ancestor::li[contains(@class, "item")]/a/@href)[position() <= 3]').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.parse_product_page)


class SnorgteesFullSpider(SnorgteesCommon):
    name = "snorgtees_full"

    def parse(self, response):
        for product_url in response.xpath('//ul[@class="productListings"]/li/a/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.parse_product_page)
