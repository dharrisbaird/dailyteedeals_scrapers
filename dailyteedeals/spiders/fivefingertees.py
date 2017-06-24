from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


# Must use www. in shopify domain

class FivefingerteesDealSpider(ShopifyCollectionSpider):
    name = "fivefingertees_deal"
    shopify_domain = 'www.fivefingertees.com'
    shopify_collections = ['daily-steal']


class FivefingerteesFullSpider(ShopifyCollectionSpider):
    name = "fivefingertees_full"
    shopify_domain = 'www.fivefingertees.com'
