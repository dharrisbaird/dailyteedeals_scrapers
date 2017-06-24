# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import Join
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from dailyteedeals.item_loaders.product import ProductItemLoader


class OtherteesDealSpider(scrapy.Spider):
    name = "othertees_deal"
    allowed_domains = ["othertees.com"]
    start_urls = ['http://www.othertees.com']

    def parse(self, response):
        for sel in response.xpath('//div[contains(@id, "design-") and contains(@class, "col-md-")]'):
            loader = ProductItemLoader(response=response, selector=sel)
            loader.add_xpath('name', './/h4/text()')
            loader.add_value('url', response.url)
            loader.add_xpath('image_url', './/img[@class="img-responsive"]/@src')
            loader.add_xpath('artist_name', './/a[contains(@href, "/profile/")]/text()')
            loader.add_xpath('prices', './/div[contains(@class, "product-price")]//text()', Join(separator=u''))
            loader.add_xpath('fabric_colors', './/option[@data-color]/@data-color')

            yield loader.load_item()

class OtherteesFullSpider(CrawlSpider):
    name = "othertees_full"
    allowed_domains = ["othertees.com"]
    start_urls = ['http://www.othertees.com/shop/clothes/']
    rules = (
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="pagination"]/li/a[@aria-label="Next"]')), follow=True),
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@href, "product")]')), callback='parse_listings'),
	)

    def parse_listings(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '(//div[@id="shop-slider"]//li)[2]/img/@src')
        loader.add_xpath('artist_name', '//div[@id="author"]/a/@title')
        loader.add_xpath('artist_urls', '//div[@id="author"]//a/@href')
        loader.add_xpath('prices', '//div[@class="shop-price"]//text()', Join())
        loader.add_xpath('fabric_colors', '//div[@class="colours"]//input/@data-color')
        loader.add_xpath('tags', '//ul[@class="tags"]//a/text()')
        return loader.load_item()
