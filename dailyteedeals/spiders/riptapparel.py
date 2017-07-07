import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urlparse
from dailyteedeals.items import ProductItemLoader


class RiptapparelCommon(scrapy.Spider):
    allowed_domains = ["riptapparel.com"]

    def parse_product_page(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//img[contains(@src, "detail")]/@src')
        loader.add_xpath('image_url', '//img[contains(@src, "1024x1024")]/@src')
        loader.add_xpath('artist_name', '//a[contains(@href, "/pages/member/")]/text()')
        loader.add_xpath('prices', '(//span[@class="price"])[1]/text()')
        return loader.load_item()


class RiptapparelDealSpider(RiptapparelCommon):
    name = "riptapparel_deal"
    start_urls = ['https://www.riptapparel.com',
                  'https://www.riptapparel.com/pages/last-call']

    def parse(self, response):
        for product_url in response.xpath('//p/a[contains(@href, "/collections/")]/@href').extract():
            yield scrapy.Request(urlparse.urljoin(response.url, product_url),
                                 callback=self.parse_product_page)



class OtherteesFullSpider(CrawlSpider, RiptapparelCommon):
    name = "riptapparel_full"
    start_urls = ['https://www.riptapparel.com/collections/mens-t-shirts']

    rules = (
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//span[@class="next"]/a')), follow=True),
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@href, "?product=Mens")]')), callback='parse_product_page'),
	)
