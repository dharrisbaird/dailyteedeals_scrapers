# -*- coding: utf-8 -*-
import scrapy
import urlparse
from dailyteedeals.items import ProductItemLoader


class YeteeCommon(scrapy.Spider):
    allowed_domains = ["theyetee.com"]

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//section[@class="product-detail-info"]/h2/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('artist_name', '//div[@class="product-artist"]/a/text()')
        loader.add_xpath('image_url', '//meta[@property="og:image"]/@content')
        loader.add_xpath('prices', '//meta[@property="og:price:amount"]/@content')

        artist_url = urlparse.urljoin(response.url, response.xpath('//div[@class="product-artist"]/a/@href').extract_first())
        request = scrapy.Request(artist_url, callback=self.parse_artist_page, dont_filter=True)
        request.meta['item'] = loader.load_item()
        yield request

    def parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_urls', '//div[@class="links"]/a/@href')
        return loader.load_item()

class YeteeDealSpider(YeteeCommon):
    name = "yetee_deal"
    start_urls = ['http://www.theyetee.com']

    def parse(self, response):
        for product_url in response.xpath('//div[@class="controls"]//a[contains(@class, "btn")]/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url), callback=self.parse_product_page)

class YeteeFullSpider(YeteeCommon):
    name = "yetee_full"
    start_urls = ['https://theyetee.com/shop/load_more.php?page=%s&view=all&category=3&order=datedesc' % page for page in xrange(1,20)]

    def parse(self, response):
        for product_url in response.xpath('//a/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.parse_product_page)
