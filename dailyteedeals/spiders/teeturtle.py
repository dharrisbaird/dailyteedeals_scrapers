from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class TeeturtleCommon(ShopifyCollectionSpider):
    shopify_domain = 'teeturtle.com'

    def is_tshirt(self, product):
        options = [v for o in product['options'] for v in o['values']]
        return 'T-Shirt' in options

    def validate(self, loader, product):
        return self.is_tshirt(product)


class TeeturtleDealSpider(TeeturtleCommon):
    name = "teeturtle_deal"
    fetch_pages = 1
    product_limit = 20

    def validate(self, loader, product):
        return float(product['variants'][0]['price']) <= 13 and self.is_tshirt(product)


class TeeturtleFullSpider(TeeturtleCommon):
    name = "teeturtle_full"
