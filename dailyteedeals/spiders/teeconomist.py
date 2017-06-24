# -*- coding: utf-8 -*-
import urlparse
import re
import json
import jmespath
import scrapy
from scrapy.loader.processors import Join
from dailyteedeals.item_loaders.product import ProductItemLoader


class TeeconomistCommon(scrapy.Spider):
    allowed_domains = ["teeconomist.com"]

    def parse_product_page(self, response, deal=False):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//input[@name="txtSaleDesignTitle"]/@value')
        loader.add_value('url', response.url)
        loader.add_value('image_url', urlparse.urljoin(response.url, response.xpath('//div[@class="tee-des"]/a/@href').extract_first()))
        loader.add_xpath('artist_name', '//span[@id="lblArtistname"]/text()')
        loader.add_xpath('artist_urls', '//div[@class="social-icon"]/a/@href')
        loader.add_xpath('prices', '//span[@class="tagfullprice"]//text()', Join(separator=u''))
        loader.add_value('fabric_colors', self.__parse_fabric_colors(response))

        if deal:
            loader.add_xpath('expires_at', '//span[@id="lbldatetime"]/text()')

        return loader.load_item()

    def __parse_fabric_colors(self, response):
        # TODO: Use jmespath processor?
        regex = re.compile(ur'designProductImagesData = (\[{.*?}\])')
        product_json = re.search(regex, response.body_as_unicode()).group(1)
        json_response = json.loads(product_json)
        result = jmespath.search('[?productGenderId == `1`].cpCode', json_response)
        return filter(None, result)


class TeeconomistDealSpider(TeeconomistCommon):
    name = "teeconomist_deal"

    start_urls = ['https://teeconomist.com/TE/']

    def parse(self, response):
        return self.parse_product_page(response, deal=True)


class TeeconomistFullSpider(TeeconomistCommon):
    name = "teeconomist_full"

    start_urls = ['https://teeconomist.com/TE/MarketPlace.aspx']

    def parse(self, response):
        for sel in response.css('a.info'):
            product_url = sel.xpath('@href').extract_first()
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.parse_product_page)
