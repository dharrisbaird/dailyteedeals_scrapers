# -*- coding: utf-8 -*-

BOT_NAME = 'dailyteedeals'

SPIDER_MODULES = ['dailyteedeals.spiders']
NEWSPIDER_MODULE = 'dailyteedeals.spiders'

USER_AGENT = 'DailyTeeDealsBot/2.0 (+https://dailyteedeals.com/bot; support@dailyteedeals.com)'

ROBOTSTXT_OBEY = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = {
    'dailyteedeals.pipelines.DefaultValuesPipeline': 1,
    'dailyteedeals.pipelines.ValidationPipeline': 2,
    'dailyteedeals.pipelines.NameCleanupPipeline': 3,
    'dailyteedeals.pipelines.AbsoluteURLPipeline': 4,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 3600
