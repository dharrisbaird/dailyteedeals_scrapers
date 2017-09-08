from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class NaolitoCommon(ShopifyCollectionSpider):
    shopify_domain = 'naolito.com'
    shopify_collections = ['t-shirts']


class NaolitoDealSpider(NaolitoCommon):
    name = "naolito_deal"
    product_limit = 2
    shuffle_products = True


class NaolitoFullSpider(NaolitoCommon):
    name = "naolito_full"