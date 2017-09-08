# -*- coding: utf-8 -*-
import random
import urlparse
from scrapy.spiders import Spider, CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from dailyteedeals.items import ProductItemLoader


class NeatoshopCommon(Spider):
    allowed_domains = ["neatoshop.com"]

    def parse_product_page(self, response):
        artist_url = response.xpath(
            '//a[contains(@href, "/artist/")]/@href').extract_first()

        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//meta[@itemprop="name"]/@content')
        loader.add_xpath('description', '//meta[@property="og:description"]/@content')
        loader.add_xpath('fabric_colors', '//select[contains(@class, "color-tshirt")]/option/@value')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//img[@itemprop="image"]/@src')
        loader.add_xpath('prices', '//spam[@id="price"]/text()')
        loader.add_xpath('prices', '//meta[@itemprop="price"]/@content')
        loader.add_xpath('tags', '//a[contains(@href, "/tag/")]/text()')

        artist_url = response.xpath('//a[contains(@href, "/artist/")]//@href').extract_first()
        request = Request(urlparse.urljoin(response.url, artist_url), callback=self.__parse_artist_page, dont_filter=True)
        request.meta['item'] = loader.load_item()
        yield request

    def __parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_name', '//h1/a/text()')
        loader.add_xpath('artist_urls', '//li[@class="artist-url"]/a/@href')
        return loader.load_item()

class NeatoshopDealSpider(NeatoshopCommon):
    name = "neatoshop_deal"
    start_urls = ['https://www.neatoshop.com/tag/on-sale']

    def parse(self, response):
        product_urls = response.xpath('//li[@class="prod-list-item"]/a/@href').extract()
        random.shuffle(product_urls)
        for product_url in product_urls[:4]:
            yield Request(urlparse.urljoin(response.url, product_url), callback=self.parse_product_page)


class NeatoshopFullSpider(NeatoshopCommon, CrawlSpider):
    name = "neatoshop_full"
    start_urls = ['https://www.neatoshop.com/catg/Movies',
                'http://www.neatoshop.com/catg/Video-Games',
                'http://www.neatoshop.com/catg/Comics-Cartoons']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@rel="next" and not(contains(@href, "page=20"))]')), 
            callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@href, "product")]')), 
            callback='parse_product_page'),
    )