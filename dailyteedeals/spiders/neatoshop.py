# -*- coding: utf-8 -*-
import re
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.contrib.linkextractors import LinkExtractor
from dailyteedeals.items import ProductItemLoader


class NeatoshopFullSpider(CrawlSpider):
    name = "neatoshop_full"
    allowed_domains = ["neatoshop.com"]
    start_urls = ['https://www.neatoshop.com/catg/Movies',
                  'http://www.neatoshop.com/catg/Video-Games',
                  'http://www.neatoshop.com/catg/Comics-Cartoons']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=(
            '//a[@rel="next" and not(contains(@href, "page=20"))]')), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=(
            '//a[contains(@href, "product")]')), callback='parse_product_page'),
    )

    def parse_product_page(self, response):
        artist_url = response.xpath('//a[contains(@href, "/artist/")]/@href').extract_first()

        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//meta[@itemprop="name"]/@content')
        loader.add_xpath('description', '//meta[@property="og:description"]/@content')
        loader.add_xpath(
            'fabric_colors', '//select[contains(@class, "color-tshirt")]/option/@value')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//img[@itemprop="image"]/@src')
        loader.add_xpath('prices', '//meta[@itemprop="price"]/@content')
        loader.add_xpath('artist_name', '//strong[@itemprop="brand"]/text()')
        loader.add_value('artist_urls', 'https://www.neatoshop.com' + artist_url)
        loader.add_xpath('tags', '//a[contains(@href, "/tag/")]/text()')
        return loader.load_item()
