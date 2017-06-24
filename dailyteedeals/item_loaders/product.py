from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from dailyteedeals.items import Product


class ProductItemLoader(ItemLoader):
    default_item_class = Product
    default_output_processor = TakeFirst()
