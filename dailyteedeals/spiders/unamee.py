# -*- coding: utf-8 -*-
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class UnameeDealSpider(scrapy.Spider):
    name = "unamee_deal"
    allowed_domains = ["www.unamee.com"]
    start_urls = ['https://www.unamee.com']

    def parse(self, response):
        for sel in response.xpath('//div[contains(@class, "list_img")]/a/@href').extract():
            yield scrapy.Request(sel, callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//div[@class="t-shirt-design-name"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//img[contains(@data-opaque, "user_design")]/@data-opaque')
        loader.add_xpath('artist_name', '//div[@class="t-shirt-designer-name"]/text()', re='Artist : (.+)')
        loader.add_xpath('prices', '//div[@class="addtocart-tab"]/span/text()')
        loader.add_xpath('fabric_colors', '//div[@class="mens-color-box normalTip"]/@data-hex')

        return loader.load_item()
