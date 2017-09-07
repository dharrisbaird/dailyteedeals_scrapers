from dailyteedeals.spiders.shopify_collection import ShopifyCollectionSpider


class WeheartgeeksCommon(ShopifyCollectionSpider):
    shopify_domain = 'weheartgeeks.com'

    def validate(self, loader, json_response):
        return "Men's T-Shirt" in json_response['title']

    def before_save(self, loader, json_response):
        loader.replace_value('name', json_response['title'].replace(" - Men's T-Shirt", ''))
        loader.replace_value('image_url', next((x['src'] for x in json_response[
                             'images'] if 'Collection' in x['src']), json_response['images'][0]['src']))
        return loader


class WeheartgeeksFullSpider(WeheartgeeksCommon):
    name = "weheartgeeks_full"


class WeheartgeeksDealSpider(WeheartgeeksCommon):
    name = "weheartgeeks_deal"
    product_limit = 4
    shuffle_products = True
