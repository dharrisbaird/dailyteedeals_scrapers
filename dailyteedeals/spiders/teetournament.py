# -*- coding: utf-8 -*-
import re
import urlparse
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class TeetournamentSpider(scrapy.Spider):
    name = "teetournament_deal"
    allowed_domains = ["teetournament.com"]
    start_urls = ['http://www.teetournament.com']

    # TODO: Use frontpage url

    def parse(self, response):
        for sel in response.xpath('//input[@name="DesignID"]/@value'):
            product_url = 'http://www.teetournament.com/product-detail.cfm?designid=' + sel.extract()

            loader = ProductItemLoader(response=response)
            loader.add_xpath('prices', '//div[@class="price priceLeft"]/text()')
            loader.add_xpath('expires_at', 'string(//script/text())', re=r'until: (\d+)')

            request = scrapy.Request(product_url, callback=self.__parse_product_page)
            request.meta['item'] = loader.load_item()
            yield request

    def __parse_product_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('name', '//meta[@property="og:title"]/@content')
        loader.add_value('url', response.url)
        loader.add_value('image_url', urlparse.urljoin(
            response.url, response.xpath('//a[@data-title]/@href').extract_first()))

        artist_url = urlparse.urljoin(response.url, response.xpath(
            '//a[contains(@href, "artist.cfm")]/@href').extract_first())

        request = scrapy.Request(artist_url, callback=self.__parse_artist_page, dont_filter=True)
        request.meta['item'] = loader.load_item()
        yield request

    def __parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_name', '//h3/text()')
        loader.add_xpath(
            'artist_urls', '//div[@class="col-sm-4"]//a[contains(@class, "socialIcon")]/@href')
        return loader.load_item()
