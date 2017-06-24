from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class SnappykidSpider(ShopifyCollectionSpider):
    name = "snappykid_full"
    shopify_domain = 'snappykid.com'
