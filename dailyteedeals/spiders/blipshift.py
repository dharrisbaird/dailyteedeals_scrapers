# -*- coding: utf-8 -*-
import re
import scrapy
from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider
from dailyteedeals.item_loaders.product import ProductItemLoader


class BlipshiftCommon(ShopifyCollectionSpider):
    shopify_domain = 'blipshift.com'

    def before_save(self, loader, product):
        loader.replace_value('artist_name', product[
                             'body_html'], re=r'<!--\n###(.+?)\n')
        loader.add_value('artist_urls', product['body_html'])
        image_url = (x['src'] for x in product['images'])
        loader.replace_value('image_url', next(
            (x for x in image_url if 'detail' in x), None))
        return loader


class BlipshiftDealSpider(BlipshiftCommon):
    name = "blipshift_deal"
    shopify_collections = ['frontpage']


class BlipshiftFullSpider(BlipshiftCommon):
    name = "blipshift_full"
