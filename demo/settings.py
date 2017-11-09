BOT_NAME = 'Scrapy'
LOG_LEVEL = 'INFO'

FEED_FORMAT = 'csv'
FEED_URI = './output/%(name)s_%(time)s.csv'

COOKIES_ENABLED = True
COOKIES_DEBUG = True

CONCURRENT_ITEMS = 500

SPIDER_MODULES = ['demo.spiders']
NEWSPIDER_MODULE = 'demo.spiders'

CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS = 1

USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0"

ITEM_PIPELINES = {}

EXTENSIONS = {}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 300,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 301
}


RETRY_HTTP_CODES = [400, 403, 407, 408, 429, 500, 502, 503, 504, 405, 503]
ENABLE_REQUESTS_STATS = False
