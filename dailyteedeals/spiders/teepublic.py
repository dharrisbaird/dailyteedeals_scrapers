# -*- coding: utf-8 -*-
import random
import urlparse
from scrapy.spiders import Spider, CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from dailyteedeals.items import ProductItemLoader


class TeepublicCommon(Spider):
    allowed_domains = ["teepublic.com"]

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)

        default_color = response.xpath('//span[@class="color-name"]/text()').extract_first().strip()
        artist_url = response.xpath('//a[contains(@href, "/user/")]/@href').extract_first()

        loader.add_xpath('name', '//meta[@property="og:title"]/@content', re=r'(.*?) by ')
        loader.add_xpath('description', '//div[contains(@class, "product-description")]/p/text()')
        loader.add_xpath('fabric_colors', '//div[@class="design-show-color"]/label/@for')
        loader.add_value('url', response.url)
        loader.add_xpath(
            'image_url', '//span[contains(@class, "color-box") and @title="%s"]/@data-preview' % default_color)
        loader.add_xpath('prices', '//meta[@property="og:price:amount"]/@content')
        loader.add_xpath('artist_name', '//meta[@property="og:title"]/@content', re=r' by (.*)$')
        loader.add_value('artist_urls', 'https://www.teepublic.com' + artist_url)
        loader.add_xpath('tags', '//div[contains(@class, "tags")]/a/text()')
        return loader.load_item()

class TeepublicDealSpider(TeepublicCommon):
    name = "teepublic_deal"
    start_urls = ['https://www.teepublic.com/t-shirts?canvas_subclass=classic-t-shirt&gender=mens&page=1&sort=newest']

    def parse(self, response):
        product_urls = response.xpath('//span[@class="sale-count-down"]/ancestor::div[contains(@class, "design-container")]//a[contains(@class, "mockup")]/@href').extract()
        random.shuffle(product_urls)
        for product_url in product_urls[:4]:
            yield Request(urlparse.urljoin(response.url, product_url), callback=self.parse_product_page)


class TeepublicFullSpider(TeepublicCommon, CrawlSpider):
    name = "teepublic_full"
    start_urls = ['https://www.teepublic.com/t-shirts/pop-culture']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=(
            '//a[@rel="next" and not(contains(@href, "page=100"))]')), follow=True),
        Rule(LinkExtractor(allow=('^https://www.teepublic.com/t-shirt/\\d+')),
             callback='parse_product_page'),
    )