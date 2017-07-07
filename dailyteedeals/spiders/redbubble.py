# -*- coding: utf-8 -*-
import re
import random
import scrapy
from scrapy.loader.processors import MapCompose
import json
import jmespath
from furl import furl
from dailyteedeals.items import ProductItemLoader


class RedbubbleFullSpider(scrapy.Spider):
    name = "redbubble_full"
    allowed_domains = ["redbubble.com"]
    start_urls = ['https://www.redbubble.com/settings/show_locale']

    URL_TEMPLATE = 'https://www.redbubble.com/shop/top+selling+geek+unisex-tshirts?page=%d'

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'settings_locale': 'en', 'settings_country_code': 'US',
                      'settings_currency_iso': 'USD'},
            callback=self.after_setup_locale)

    def after_setup_locale(self, response):
        for page in range(1, 15):
            yield scrapy.Request(self.URL_TEMPLATE % page, callback=self.__parse_list_page)

    def __parse_list_page(self, response):
        for path in response.xpath('//a[contains(@class, "grid-item")]/@href').extract():
            yield scrapy.Request('https://www.redbubble.com' + path, callback=self.__parse_product_page)

    def __parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h2[@class="work-information_title"]/text()')
        loader.add_xpath('description', '//meta[@name="product:price:amount"]/@content')
        loader.add_value('url', response.url)
        loader.add_value('image_url', response.body, re=r'https:\/\/[\w|\.]+\/[\w|.]+\/raf.*?\.jpg')
        loader.add_xpath('prices', '//meta[@property="product:price:amount"]/@content')
        loader.add_xpath('artist_name', '//a[@rel="author"]/text()')
        loader.add_xpath('artist_urls', '//a[@rel="author"]/@href')
        loader.add_xpath('tags', '//p[@class="description_tag-list"]/a/text()',
                         output_processor=MapCompose(lambda x: x.split(',')))

        return loader.load_item()


#
#     def parse(self, response):
# https://www.redbubble.com/shop/top%20selling+geek+unisex-tshirts
#
#         response.selector.remove_namespaces()
#         for sel in response.xpath('//entry'):
#             f = furl(sel.xpath('.//link[@rel="alternate"]/@href').extract_first())
#             f.args['p'] = 't-shirt'
#
#             loader = ProductItemLoader(response=response, selector=sel)
#             loader.add_xpath('name', './/title/text()')
#             loader.add_value('url', f.url)
#             loader.add_xpath('tags', './/category/@term')
#             loader.add_value('artist_name', self.artist_url, re=r'people\/([\w|\d|-]+)')
#             loader.add_value('artist_urls', self.artist_url)
#
#             f.path = f.path.__str__() + '.json'
#             f.args['country_code'] = 'US'
#
#             request = scrapy.Request(f.url, callback=self.__parse_product_json)
#             request.meta['item'] = loader.load_item()
#             yield request
#
#     def __parse_product_json(self, response):
#         jsonresponse = json.loads(response.body_as_unicode())
#
#         item = response.meta['item']
#         loader = ProductItemLoader(item, response=response)
#         loader.add_value('prices', jmespath.search(
#             'product_configuration.price.amount', jsonresponse))
#         loader.add_value('fabric_colors', jmespath.search(
#             'product_configuration.options.colors[*].hex', jsonresponse))
#
#         f = furl(response.url)
#         f.args['body_color'] = self.__random_product_color(jsonresponse)
#
#         request = scrapy.Request(f.url, callback=self.__generate_image_url)
#         request.meta['item'] = loader.load_item()
#         yield request
#
#     def __random_product_color(self, jsonresponse):
#         color_names = jmespath.search('product_configuration.options.colors[*].value', jsonresponse)
#         excluded = ['black', 'white', 'charcoal_heather', 'heather_grey']
#         viable_colors = filter(lambda s: not any(x in s for x in excluded), color_names)
#         if not viable_colors:
#             viable_colors = color_names
#         return random.choice(viable_colors)
#
#     def __generate_image_url(self, response):
#         jsonresponse = json.loads(response.body_as_unicode())
#
#         image_url = jmespath.search(
#             "work_closeup_images[?title == 'Design'].url | [0]", jsonresponse)
#         dimensions = re.findall(r'(\d+x\d+)', image_url)[0].split('x')
#         dimensions = [int(numeric_string) for numeric_string in dimensions]
#         ratio = float(self.MAX_IMAGE_SIZE) / max(dimensions)
#         new_dimensions = 'x'.join([str(int(v * ratio)) for v in dimensions])
#         new_image_url = re.sub(r'(\d+x\d+)', new_dimensions, image_url)
#
#         item = response.meta['item']
#         loader = ProductItemLoader(item, response=response)
#         loader.add_value('image_url', new_image_url)
#
#         yield loader.load_item()
