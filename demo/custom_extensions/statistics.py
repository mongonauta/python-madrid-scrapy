import logging

from scrapy import signals


class StatsExtension(object):
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        # return the extension object
        return ext

    def spider_closed(self, spider):
        if spider.cache_info:
            logging.info("Calculating spider run statistics now")
            self.stats = spider.crawler.stats

            self.stats.set_value("stat/AVG/rooms", round(
                reduce((lambda x, y: x + y), spider.cache_info['rooms']) / len(spider.cache_info['rooms']),
                2
            ))

            avg_price = reduce((lambda x, y: x + y), spider.cache_info['prices']) / len(spider.cache_info['prices'])
            self.stats.set_value("stat/AVG/price", round(avg_price, 2))

            avg_square_meters = reduce(
                (lambda x, y: x + y), spider.cache_info['square_meters']
            ) / len(spider.cache_info['square_meters'])
            self.stats.set_value("stat/AVG/square_meters", round(avg_square_meters, 2))

            self.stats.set_value("stat/price_per_square_meters", round(avg_price/avg_square_meters, 2))
