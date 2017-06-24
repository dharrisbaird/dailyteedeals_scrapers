import re
from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class NaolitoFullSpider(ShopifyCollectionSpider):
    name = "naolito_full"
    shopify_domain = 'naolito.com'
