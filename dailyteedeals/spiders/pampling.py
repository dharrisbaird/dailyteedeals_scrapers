# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import Join
from dailyteedeals.items import ProductItemLoader


class PamplingSpider(scrapy.Spider):
    name = "pampling_deal"
    allowed_domains = ["pampling.com"]
    start_urls = ['http://www.pampling.com']

    def parse(self, response):
        for product_url in response.xpath('//a[contains(@href, "productos") and @class="btn btn-ficha"]/@href').extract():
            loader = ProductItemLoader(response=response)
            loader.add_xpath('expires_at', '//input[@id="segundos_restantes"]/@value')
            request = scrapy.Request(product_url, callback=self.__parse_product_page)
            request.meta['item'] = loader.load_item()
            yield request

    def __parse_product_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('name', '//div[@id="datos_autor"]/h2/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('artist_name', '//div[@id="datos_autor"]/a/text()')
        loader.add_xpath('image_url', '//div[@id="contenedor_fotos"]/div[2]/img/@data-src')
        loader.add_xpath('prices', '//div[@class="precio-xt-euros"]//text()', Join())
        return loader.load_item()
