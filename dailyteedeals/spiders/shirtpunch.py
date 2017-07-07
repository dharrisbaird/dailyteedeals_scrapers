# -*- coding: utf-8 -*-
import scrapy
from dailyteedeals.items import ProductItemLoader


class ShirtpunchCommon(scrapy.Spider):
    allowed_domains = ["shirtpunch.com"]

    def loop_products(self, response, selector, deal):
        for sel in response.css(selector):
            loader = ProductItemLoader(response=response)

            if deal:
                loader.add_xpath('expires_at', 'string(//body)', re='clock.setTime\((.*?)\)')

            request = scrapy.Request(sel.xpath('@href').extract_first(),
                                     callback=self.__parse_product_page)
            request.meta['item'] = loader.load_item()
            yield request

    def __parse_product_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//img[@class="gallery-image"]/@src')
        loader.add_xpath('artist_name', '//span[@class="designer-name"]/text()')
        loader.add_value('artist_name', 'ShirtPunch')
        loader.add_xpath('artist_urls', '//div[@class="designer-links"]/a/@href')
        loader.add_xpath('prices', '//span[@class="price"]/text()')
        return loader.load_item()


class ShirtpunchDealSpider(ShirtpunchCommon):
    name = "shirtpunch_deal"
    start_urls = (
        'https://www.shirtpunch.com',
    )

    def parse(self, response):
        return self.loop_products(response, '.daily-features>div>a', True)


class ShirtpunchFullSpider(ShirtpunchCommon):
    name = "shirtpunch_full"
    start_urls = (
        'https://www.shirtpunch.com/tees.html?limit=36',
    )

    def parse(self, response):
        return self.loop_products(response, 'a.product-link', False)
