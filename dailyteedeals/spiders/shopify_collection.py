import json
import random
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class ShopifyCollectionSpider(scrapy.Spider):
    """ Shopify spider which parses product and collection feeds to discover prodducts. 
    
    Attributes:
        shopify_domain (str): 
        product_limit (Optional[int]): The maximum products to fetch, -1 for unlimited.
        collection_limit (Optional[int]): Human readable string describing the exception.
        shuffle_products (Optional[bool]): Whether products should be shuffled.
    """

    COLLECTION_ENDPOINT = 'http://%s/collections/%s/products.json?limit=250&page=%d'
    PRODUCTS_ENDPOINT = 'http://%s/products.json?limit=250&page=%d'

    shopify_domain = None
    product_limit = -1
    collection_limit = 5
    shuffle_products = False

    def __init__(self, *a, **kw):
        if self.shopify_domain is None:
            raise NotImplementedError('shopify_domain not defined in spider')

        self.allowed_domains = [self.shopify_domain]
        super(ShopifyCollectionSpider, self).__init__(*a, **kw)

    def start_requests(self):
        if hasattr(self, 'shopify_collections'):
            for slug in self.shopify_collections:
                print "Getting collection: " + slug
                collection_url = ShopifyCollectionSpider.COLLECTION_ENDPOINT % (
                    self.shopify_domain, slug, 1)
                yield scrapy.Request(collection_url, callback=self.__parse_products)
        else:
            print "Getting all collections"
            for page in xrange(self.collection_limit):
                collections_url = ShopifyCollectionSpider.PRODUCTS_ENDPOINT % (
                    self.shopify_domain, page)
                print collections_url
                yield scrapy.Request(collections_url, callback=self.__parse_products)

    def validate(self, loader, json_response):
        return True

    def before_save(self, loader, product):
        return loader

    def __parse_products(self, response):
        json_response = json.loads(response.body_as_unicode())

        if self.shuffle_products:
            random.shuffle(json_response['products'])

        added_products = 0
        for product in json_response['products']:
            if len(product['images']) == 0 or not any(v['available'] for v in product['variants']):
                continue

            if self.product_limit != -1 and added_products >= self.product_limit:
                break

            loader = ProductItemLoader()
            loader.add_value('name', product['title'])
            loader.add_value('url', 'http://%s/products/%s' %
                             (self.shopify_domain, product['handle']))
            loader.add_value('image_url', product['images'][0]['src'])
            loader.add_value('artist_name', product['vendor'])
            loader.add_value('prices', '$' + product['variants'][0]['price'])
            loader.add_value('tags', product['tags'])
            loader = self.before_save(loader, product)
            if self.validate(loader, product):
                yield loader.load_item()
                added_products += 1
