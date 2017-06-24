import re
from scrapy.selector import Selector
from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider
from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider
from dailyteedeals.item_loaders.product import ProductItemLoader


class ShirtbattleCommon(ShopifyCollectionSpider):
    shopify_domain = 'shirtbattle.com'

    def before_save(self, loader, product):
        body = Selector(text=product['body_html'])
        loader.replace_value('artist_name', body.xpath('//h1/span/text()').extract_first())
        loader.replace_value('artist_urls', body.xpath('//a/@href').extract())
        return loader


class ShirtbattleDealSpider(ShirtbattleCommon):
    name = "shirtbattle_deal"
    shopify_collections = ['frontpage']


class ShirtbattleFullSpider(ShirtbattleCommon):
    name = "shirtbattle_full"
