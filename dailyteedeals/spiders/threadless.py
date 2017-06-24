# -*- coding: utf-8 -*-
import urlparse
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dailyteedeals.item_loaders.product import ProductItemLoader


class ThreadlessCommon(CrawlSpider):
    allowed_domains = ["threadless.com"]

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//div[@class="product_identity clearfix"]/h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//a[@class="design" and contains(@href, "design")]/@href')
        loader.add_xpath('artist_name', '//p[@class="tip"]/@data-title')
        loader.add_xpath('prices', '//div[@data-glname="Mens Tee"]/@data-glprice')
        loader.add_xpath('prices', '//div/@data-glprice')

        artist_url = response.xpath('//p[@class="tip"]/a/@href').extract_first()
        request = scrapy.Request(urlparse.urljoin(response.url, artist_url),
                                 callback=self.parse_artist_page,
                                 dont_filter=True)
        request.meta['item'] = loader.load_item()
        yield request

    def parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_urls', '//div[@class="profile-info"]//a/@href')
        return loader.load_item()


class ThreadlessDealSpider(ThreadlessCommon):
    name = "threadless_deal"
    start_urls = ['https://www.threadless.com/catalog/price,13/style,tees/type,guys/view,24/order,new/category,Film']

    def parse(self, response):
        for product_url in response.xpath('//dd[@class="product_item"]/a/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.parse_product_page)

class ThreadlessFullSpider(ThreadlessCommon):
    name = "threadless_full"
    start_urls = ['https://www.threadless.com/catalog/style,tees/type,guys/view,48/display,hero/order,popular/']
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="next"]/a')), follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//dd[@class="product_item"]/a')), callback='parse_product_page'),
    )
