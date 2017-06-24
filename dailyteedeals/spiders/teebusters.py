# -*- coding: utf-8 -*-
import scrapy
from dailyteedeals.item_loaders.product import ProductItemLoader


class TeebustersDealSpider(scrapy.Spider):
    name = "teebusters_deal"
    allowed_domains = ["teebusters.com"]
    start_urls = (
        'https://teebusters.com',
        'https://teebusters.com/index/lastchance.html'
    )

    def parse(self, response):
        loader = ProductItemLoader(response=response)
        loader.add_xpath('name', '//div[@id="app_info"]/strong/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('image_url', '//img[contains(@src, "zoom")]/@src')
        loader.add_xpath('artist_name', '//div[@id="profile-box"]//strong/text()')
        loader.add_xpath('artist_urls', '//a[@class="followBox"]/@href')
        loader.add_value('prices', '8.99 EUR')
        loader.add_value('last_chance', response.url == 'https://teebusters.com/index/lastchance.html')
        loader.add_xpath('expires_at', 'string(//script/text())', re=r'until: (\d+)')

        return loader.load_item()
