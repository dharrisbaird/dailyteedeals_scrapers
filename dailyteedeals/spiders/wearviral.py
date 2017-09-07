from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class WearviralCommon(ShopifyCollectionSpider):
    shopify_domain = 'wearviral.com'

    def before_save(self, loader, product):
        loader.replace_value('artist_name', 'Wear Viral')
        return loader


class WearviralDealSpider(WearviralCommon):
    name = "wearviral_deal"
    shopify_collections = ['best-sellers']

    def validate(self, loader, json_response):
        return json_response['variants'][0]['price'] < 15



class WearviralFullSpider(WearviralCommon):
    name = "wearviral_full"
