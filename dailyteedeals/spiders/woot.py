# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dailyteedeals.item_loaders.product import ProductItemLoader


class WootCommon(CrawlSpider):
    allowed_domains = ["shirt.woot.com"]

    def parse_product_page(self, response):
        print response.url
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//span[@itemprop="name"]/text()', re=r'(.+) by')
        loader.add_value('url', response.url)
        loader.add_xpath('artist_name', '//aside[@class="artist-info"]//h2/text()')
        loader.add_xpath('artist_name', '//span[@itemprop="name"]/text()', re=r'\sby\s(.+)')
        loader.add_xpath('image_url', '(//div[@data-zoom-url]/@data-zoom-url)[last()]')
        loader.add_xpath('prices', '//div[@itemprop="priceSpecification"]/span[@itemprop="minPrice" or @itemprop="price"]/text()')
        return loader.load_item()

    def find_image_url(self, response):
        widths = response.xpath('//div/@data-zoom-width').extract()
        largest_width = max(widths, key=lambda x: int(x))
        return response.xpath('//div[@data-zoom-width="%s"]/@data-zoom-url' % largest_width).extract_first()

class WootDealSpider(WootCommon):
    name = "woot_deal"
    start_urls = ['http://shirt.woot.com']

    def parse(self, response):
        product_url = response.xpath('//a[contains(@class, "wantone")]/@href').extract_first()
        request = scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.parse_product_page)
        return request

class WootFullSpider(WootCommon):
    name = "woot_full"
    start_urls = ['http://shirt.woot.com/catalog?ref=sh_sh_ctlg']
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('(//a[@class="next"])[1]')), follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@href, "offers")]')), callback='parse_product_page'),
    )
