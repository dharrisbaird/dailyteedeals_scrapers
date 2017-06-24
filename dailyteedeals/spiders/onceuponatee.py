import re
from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class OnceuponateeCommon(ShopifyCollectionSpider):
    shopify_domain = 'onceuponatee.net'

    def validate(self, loader, product):
        return any('T-Shirt' in v['title'] for v in product['variants']) and \
            'collection' not in product['title'].lower()

    def before_save(self, loader, product):
        title = product['title'].rsplit('-', 1)[0]

        # Fix artist name
        artist = product['vendor'].rsplit('-', 1)[0]

        loader.replace_value('name', re.sub('\(.*?\)', '', title))
        loader.replace_value('artist_name', artist)
        return loader


class OnceuponateeDealSpider(OnceuponateeCommon):
    name = "onceuponatee_deal"
    shopify_collections = ['current-collection']
    product_limit = 10
    shuffle_products = True


class OnceuponateeFullSpider(OnceuponateeCommon):
    name = "onceuponatee_full"
