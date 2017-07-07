BOT_NAME = 'dailyteedeals'

SPIDER_MODULES = ['dailyteedeals.spiders']
NEWSPIDER_MODULE = 'dailyteedeals.spiders'

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
    'dailyteedeals.pipelines.ParseMoneyPipeline': 5,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 3600
