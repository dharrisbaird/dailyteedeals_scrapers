# -*- coding: utf-8 -*-
import urlparse
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class QwerteeCommon(scrapy.Spider):
    allowed_domains = ["qwertee.com"]

    def build_currency_string(self, doc, currency):
        return self.__extract_currency(doc, currency) + currency.upper()

    def __extract_currency(self, doc, currency):
        return doc.xpath('@data-tee-price-' + currency).extract_first()

    def parse_artist_page(self, response):
        item = response.meta['item']
        loader = ProductItemLoader(item, response=response)
        loader.add_xpath('artist_urls', '//div[@id="page-header"]/span/text()')
        return loader.load_item()

    def build_image_url(self, product_id):
        return 'https://www.qwertee.com/images/designs/zoom/%s.jpg' % product_id


class QwerteeDealSpider(QwerteeCommon):
    name = "qwertee_deal"
    start_urls = ['https://www.qwertee.com']

    def parse(self, response):
        expiry = response.xpath('//div[@class="index-countdown"]/@data-time').extract_first()

        for index, sel in enumerate(response.css('.big-slide.tee > div')):
            product_id = sel.xpath('@data-id').extract_first()

            artist_id = sel.xpath('@data-user-id').extract_first()
            currencies = [self.build_currency_string(sel, c)
                          for c in ['usd', 'gbp', 'eur']]

            loader = ProductItemLoader(response=response, selector=sel)
            loader.add_xpath('name', '@data-name')
            loader.add_value('url', response.url)
            loader.add_value('image_url', self.build_image_url(product_id))
            loader.add_xpath('artist_name', '@data-user')
            loader.add_value('prices', ' / '.join(currencies))
            loader.add_value('last_chance', index > 2)
            loader.add_value('expires_at', expiry)

            request = scrapy.Request(urlparse.urljoin(response.url, '/profile/' + artist_id),
                                     callback=self.parse_artist_page,
                                     dont_filter=True)
            request.meta['item'] = loader.load_item()
            yield request


class QwerteeFullSpider(QwerteeCommon):
    name = "qwertee_full"
    start_urls = (
        'https://www.qwertee.com/shop/all',
    )

    def parse(self, response):
        for sel in response.css('.tee-list-item>a'):
            product_url = sel.xpath('@href').extract_first()
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        if '/product/' in response.url:
            product_id = response.xpath('//a[contains(@class, "buy-button")]/@data-id').extract_first()
            artist = response.xpath('//span[@class="author"]/a')
            currency_sel = response.xpath('//p[@class="product-price"]')
            currencies = [self.build_currency_string(currency_sel, c)
                          for c in ['usd', 'gbp', 'eur']]

            loader = ProductItemLoader(response=response)
            loader.add_xpath('name', '//span[@class="name"]/text()')
            loader.add_value('url', response.url)
            loader.add_value('image_url', self.build_image_url(product_id))
            loader.add_value('artist_name', artist.xpath('text()').extract())
            loader.add_value('prices', ' / '.join(currencies))
            loader.add_value('last_chance', response.url == 'https://www.qwertee.com/last-chance')

            request = scrapy.Request(urlparse.urljoin(response.url, artist.xpath('@href').extract_first()),
                                     callback=self.parse_artist_page,
                                     dont_filter=True)
            request.meta['item'] = loader.load_item()
            return request
