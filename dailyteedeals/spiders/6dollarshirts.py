# -*- coding: utf-8 -*-
import re
import urlparse
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dailyteedeals.items import ProductItemLoader


class SixDollarShirtCommon(CrawlSpider):
    allowed_domains = ["6dollarshirts.com"]

    def parse_product_page(self, response):
        image_url = response.xpath('//meta[@property="og:image"]/@content').extract_first()
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_value('image_url', image_url.replace('400x400', '750x750'))
        loader.add_xpath('fabric_colors', '//img[contains(@src, "swatches")]/@alt')
        loader.add_value('artist_name', '6 Dollar Shirts')
        loader.add_value('artist_urls', ['http://6dollarshirts.com/'])
        loader.add_value('prices', '$6')
        return loader.load_item()


class SixDollarShirtDealSpider(SixDollarShirtCommon):
    name = "6dollarshirts_deal"
    start_urls = ['http://www.6dollarshirts.com']

    def parse(self, response):
        for url in response.xpath('(//div[@class="image"]/a/@href)[1]').extract():
            yield scrapy.Request(url, callback=self.parse_product_page)


class SixDollarShirtFullSpider(SixDollarShirtCommon):
    name = "6dollarshirts_full"
    start_urls = ['http://6dollarshirts.com/guys-tees']
    rules = (
        # Extract links for next pages
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[text()=">"]')), follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=(
            '//div[@class="image"]/a')), callback='parse_product_page'),
    )
