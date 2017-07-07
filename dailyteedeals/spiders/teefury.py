# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dailyteedeals.items import ProductItemLoader

class TeefuryCommon(CrawlSpider):
    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//meta[@property="og:title"]/@content')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//div[contains(@class,"artwork-slide")]/@data-full-image')
        loader.add_xpath('artist_name', '//h2[@class="artist-name"]//span/text()')

        loader.add_xpath('prices', '(//span[@itemprop="price"])[1]/text()')
        loader.add_value('prices', response.body, re=r'ecomm_totalvalue: (\d+)')
        loader.add_value('last_chance', loader.get_output_value('prices') == '14')

        artist_url = response.xpath('//h2[@class="artist-name"]//a/@href').extract_first()
        request = scrapy.Request(artist_url, callback=self.parse_artist_page, dont_filter=True)
        request.meta['item'] = loader.load_item()
        yield request

    def parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_urls', '//div[contains(@class, "category-userprofile-info")]//a/@href')
        return loader.load_item()

class TeefuryDealSpider(TeefuryCommon):
    name = "teefury_deal"
    allowed_domains = ["www.teefury.com"]
    start_urls = ['http://www.teefury.com', 'http://www.teefury.com/afterhours']

    def parse(self, response):
        for product_url in response.xpath('//meta[@itemprop="url"]/@content').extract():
            yield scrapy.Request(product_url, callback=self.parse_product_page)

class TeefuryFullSpider(TeefuryCommon):
    name = "teefury_full"
    allowed_domains = ["www.teefury.com"]
    start_urls = ['http://www.teefury.com/tees']
    rules = (
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="next"]')), follow=True),
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@itemprop="url"]')), callback='parse_product_page'),
	)
