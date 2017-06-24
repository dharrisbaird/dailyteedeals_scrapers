import re
from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class PopupteeCommon(ShopifyCollectionSpider):
    shopify_domain = 'popuptee.com'

    def before_save(self, loader, product):
        title = product['title']
        image_url = [x['src'] for x in product['images']]
        loader.replace_value('name', re.sub('.*?\sDeal - ', '', title))
        loader.replace_value('image_url', next((x for x in image_url if '.png' in x), None))

        return loader


class PopupteeDealSpider(PopupteeCommon):
    name = "popuptee_deal"
    product_limit = 10
    shuffle_products = True
    collection_limit = 1

    def validate(self, loader, product):
        if(float(product['variants'][0]['price']) >= 15):
            return False

        return True


class PopupteeFullSpider(PopupteeCommon):
    name = "popuptee_full"
