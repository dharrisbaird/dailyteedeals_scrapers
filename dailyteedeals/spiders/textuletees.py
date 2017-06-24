from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class TextualteesSpider(ShopifyCollectionSpider):
    name = "textualtees_full"
    shopify_domain = 'textualtees.com'

    def before_save(self, loader, product):
        loader.replace_value('artist_name', 'Textualtees')
        return loader
