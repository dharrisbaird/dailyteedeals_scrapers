# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

STOPWORDS = ["gift certificate", "hoodie", "bracelet", "poster",
             "card", "monthly", "infant" "toddler", "youth", "baby",
             "onesie", "sock", "beanie", "hat"]

IGNORED_WORDS = ["tee", "tshirt", "t-shirt", "shirt", "reprint"]


class DefaultValuesPipeline(object):

    def process_item(self, item, spider):
        spider_type = spider.name.rsplit('_', 1)[1]

        item.setdefault('active', True)
        item.setdefault('valid', True)
        item.setdefault('last_chance', False)
        item.setdefault('deal', spider_type == 'deal')
        item.setdefault('tags', [])
        item.setdefault('fabric_colors', [])
        item.setdefault('stopwords', [])
        return item


class ValidationPipeline(object):
    REQUIRED_FIELDS = ['name', 'artist_name']

    def process_item(self, item, spider):
        for field in self.REQUIRED_FIELDS:
            if not item[field]:
                item['valid'] = False

        words = item['name'].lower().split()
        item['stopwords'] = set(words).intersection(STOPWORDS)

        return item


class NameCleanupPipeline(object):
    def process_item(self, item, spider):
        item['name'] = item['name'].lower()
        for word in IGNORED_WORDS:
            item['name'] = item['name'].replace(word, '')
        return item

class AbsoluteURLPipeline(object):
    def process_item(self, item, spider):
        for field in ['url', 'image_url']:
            if len(spider.start_urls) > 0:
                item[field] = urljoin(spider.start_urls[0], item[field])
        return item
