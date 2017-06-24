from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class FandomshirtsSpider(ShopifyCollectionSpider):
    name = "fandomshirts_deal"
    shopify_domain = 'fandomshirts.com'

    def before_save(self, loader, product):
        loader.replace_value('tags', [])
        return loader
