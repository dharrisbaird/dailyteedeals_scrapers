# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import Identity
from dailyteedeals.item_loaders.processors import ExtractUrls, ParseDate


class Product(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    artist_name = scrapy.Field()
    artist_urls = scrapy.Field(output_processor=ExtractUrls())
    prices = scrapy.Field()
    deal = scrapy.Field()
    active = scrapy.Field()
    last_chance = scrapy.Field()
    valid = scrapy.Field()
    expires_at = scrapy.Field(input_processor=ParseDate())
    fabric_colors = scrapy.Field(output_processor=Identity())
    tags = scrapy.Field(output_processor=Identity())
