# -*- coding: utf-8 -*-
import re
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule, Request
from scrapy.contrib.linkextractors import LinkExtractor
from dailyteedeals.item_loaders.product import ProductItemLoader


class Society6FullSpider(CrawlSpider):
    name = "society6_full"
    allowed_domains = ["society6.com"]
    start_urls = ['https://society6.com/tshirts/movies-tv']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=(
            '//a[contains(@href, "?page=") and contains(text(), "Next")]')), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=(
            '//a[@data-dmc="prod-title"]')), callback='parse_product_page'),
    )

    def parse_product_page(self, response):
        print_url = response.xpath('//a[text()="Art Print"]/@href').extract_first()
        username = response.xpath('//div[@class="user-avatar"]/a/@href').extract_first()

        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1[@data-dmc="prod-name"]/text()')
        loader.add_xpath('description', '//p[@id="about-the-art-description"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('prices', '//meta[@itemprop="price"]/@content')
        loader.add_xpath('artist_name', '//h1[@data-dmc="prod-name"]/following::a/text()')
        loader.add_value('artist_urls', 'https://society6.com' + username)
        loader.add_xpath('tags', '//p[@class="tag-container"]/a/text()')
        loader.add_value('active', response.xpath(
            '//meta[@property="og:availability"]/@content').extract_first() == 'instock')

        request = Request(urlparse.urljoin(response.url, print_url), callback=self.parse_image)
        request.meta['item'] = loader.load_item()
        return request

    def parse_image(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)

        regex = re.compile(r'"full":{"url":"(http.*?artwork\\/~artwork.*?)"')
        url = re.search(regex, response.body_as_unicode()).group(1).replace('\\', '')

        loader.add_value('image_url', url)

        return loader.load_item()
