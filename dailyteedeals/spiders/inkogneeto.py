# -*- coding: utf-8 -*-
import urlparse
import scrapy
from dailyteedeals.items import ProductItemLoader


class InkogneetoSpider(scrapy.Spider):
    name = "inkogneeto_deal"
    allowed_domains = ["inkogneeto.com"]
    start_urls = ['http://www.inkogneeto.com']

    def parse(self, response):
        for product_url in response.xpath('//a[contains(@href, "/shop/")]/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url), callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//meta[@property="og:title"]/@content')
        loader.add_value('url', response.url)
        loader.add_value('artist_name', 'Inkogneeto')
        loader.add_value('artist_urls', ['http://www.inkogneeto.com'])
        loader.add_xpath('image_url', '//div[@id="productThumbnails"]//img[contains(@data-src, "SMALL")]/@data-src')
        loader.add_xpath('prices', '//meta[@property="product:price:amount"]/@content')
        return loader.load_item()
