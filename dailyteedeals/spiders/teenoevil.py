from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class TeenoevilSpider(ShopifyCollectionSpider):
    name = "teenoevil_full"
    shopify_domain = 'teenoevil.com'

    def before_save(self, loader, product):
        images = product['images']
        found = next((obj['src']
                      for obj in images if 'design' in obj['src'].lower()), images[0]['src'])
        loader.replace_value('image_url', found)
        return loader
