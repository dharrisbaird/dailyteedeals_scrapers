# -*- coding: utf-8 -*-
import scrapy
import urlparse
from dailyteedeals.items import ProductItemLoader


class AplenteeSpider(scrapy.Spider):
    name = "aplentee_deal"
    allowed_domains = ["aplentee.com"]
    start_urls = ['http://aplentee.com']

    def parse(self, response):
        for product_url in response.xpath('//a[contains(@href, "/p/")]/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//div[@class="name"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//section[@class="product-info"]//img[1]/@ref')
        loader.add_xpath('artist_name', '//a[contains(@href, "/artists/")]/text()')
        loader.add_xpath('prices', '//span[@id="price"]/text()')

        artist_url = urlparse.urljoin(response.url, response.xpath(
            '//a[contains(@href, "/artists/")]//@href').extract_first())
        request = scrapy.Request(artist_url, callback=self.__parse_artist_page, dont_filter=True)
        request.meta['item'] = loader.load_item()
        yield request

    def __parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_urls', '//div[@class="typography"]//a/@href')
        return loader.load_item()
