# -*- coding: utf-8 -*-
import re
import scrapy
import urlparse
from dailyteedeals.item_loaders.product import ProductItemLoader


class TeevoltSpider(scrapy.Spider):
    name = "teevolt_deal"
    allowed_domains = ["teevolt.com"]
    start_urls = ['http://www.teevolt.com']

    def parse(self, response):
        for product_url in response.xpath('//div[@id="rt-maintop"]//a[contains(@href, "vote/item")]/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        artist_re = re.compile('by\s+(.+)', re.IGNORECASE)
        artist = response.xpath('//h1[@class="pos-title"]/text()').extract()
        loader.add_xpath('name', '//meta[@itemprop="itemreviewed"]/@content')
        loader.add_value('url', ['http://www.teevolt.com'])
        loader.add_xpath('image_url', '//img[contains(@src,"com_zoo")][1]/@src')
        loader.add_value('artist_name', ''.join(artist), re=artist_re)
        loader.add_xpath('artist_urls', '//div[@class="pos-description"]//a/@href')
        loader.add_value('prices', '7.50 GBP / 9 EUR / 12 USD')
        return loader.load_item()
