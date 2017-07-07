# -*- coding: utf-8 -*-
import re
import scrapy
from dailyteedeals.items import ProductItemLoader


class TeeteeCommon(scrapy.Spider):
    allowed_domains = ["teetee.eu"]

    def parse_product_page(self, response):
        prices = response.xpath(
            'string(//body)').re(r'{"variations_price":{"\d+":"(\d+\.\d{1,2})\\u20ac"')

        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1[@class="product"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//a[@data-imagelightbox="single"]/@href')
        loader.add_xpath('image_url', '//meta[@property="og:image"]/@content')
        loader.add_xpath('artist_name', '//h2[@class="product"]/a/text()')
        loader.add_xpath('artist_urls', '//div[@data-show-all-content]//a/@href')
        loader.add_value('prices', prices[0] + u' €')
        loader.add_value('last_chance', response.url == 'http://www.teetee.eu/en/overtime')
        loader.add_xpath('expires_at', 'string(//body)', re=(r'EXPIRE_DATE = "(.*?)";'))

        return loader.load_item()


class TeeteeDealSpider(TeeteeCommon):
    name = "teetee_deal"
    start_urls = (
        'http://www.teetee.eu/en/',
        'http://www.teetee.eu/en/overtime'
    )

    def parse(self, response):
        return self.parse_product_page(response)


class TeeteeFullSpider(TeeteeCommon):
    name = "teetee_full"

    def start_requests(self):
        formdata = {
            "type": "shop",
            "action": 'load_more',
            "offset": "0",
            "num": "1000"
        }
        yield scrapy.FormRequest('http://www.teetee.eu/wp/wp-admin/admin-ajax.php',
                                 formdata=formdata, callback=self.parse_list)

    def parse_list(self, response):
        for product_url in response.xpath('//a[contains(@href, "shop")]/@href').extract():
            yield scrapy.Request(product_url, callback=self.parse_product_page)
