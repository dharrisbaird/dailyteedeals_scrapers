# -*- coding: utf-8 -*-
import re
import scrapy
import urlparse
from dailyteedeals.items import ProductItemLoader


class MymainmanpatSpider(scrapy.Spider):
    name = "mymainmanpat_deal"
    allowed_domains = ["mymainmanpat.com"]
    start_urls = ['http://www.mymainmanpat.com']

    def parse(self, response):
        for product_link in response.xpath('//div[contains(@class, "wc-shortcodes-column")]/p/a[contains(@href, "limited-edition-hip-hop-t-shirts")]'):
            loader = ProductItemLoader(response=response)
            loader.add_value('image_url', product_link.xpath('.//img[@srcset]/@src').extract_first())

            request = scrapy.Request(product_link.xpath('@href').extract_first(), callback=self.__parse_product_page)
            request.meta['item'] = loader.load_item()
            yield request

    def __parse_product_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)

        loader.add_xpath('name', '//meta[@property="og:title"]/@content', re=r'(.*?) By')
        loader.add_value('url', response.url)
        loader.add_xpath('artist_name', '//meta[@property="og:title"]/@content', re=r'.*By\s(.+)')
        loader.add_xpath('artist_urls', '//div[@class="mini_description"]//a/@href')
        loader.add_value('prices', '$25')
        return loader.load_item()
