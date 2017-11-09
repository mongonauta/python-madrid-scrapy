import copy
import logging

from datetime import datetime

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider

from demo.items import FlatItem


class IdealistaSpider(Spider):
    name = 'idealista'
    base_url = 'https://www.idealista.com'

    neighborhoods = None
    rent_neighborhood_url_template = 'https://www.idealista.com/{type}-viviendas/{city}/{neighborhood}/'

    default_country = 'Spain'
    default_city = 'Madrid'
    default_type = 'Alquiler'

    def __init__(self, neighborhoods=None, *args, **kwargs):
        super(IdealistaSpider, self).__init__(*args, **kwargs)
        self.neighborhoods = ['san-blas'] if not neighborhoods else neighborhoods.split(',')

    def start_requests(self):
        for neighborhood in self.neighborhoods:
            url = self.rent_neighborhood_url_template.format(
                type=self.default_type.lower(),
                city=self.default_city.lower(),
                neighborhood=neighborhood
            )

            yield Request(
                url=url,
                meta={
                    'country': self.default_country,
                    'city': self.default_city,
                    'type': self.default_type,
                    'neighborhood': neighborhood
                },
                callback=self.overview
            )

    def overview(self, response):
        sel = Selector(response)
        meta = copy.deepcopy(response.meta)

        basic_item = FlatItem()

        # ITEM DEFAULT INFO
        basic_item['website'] = self.name
        basic_item['referer_url'] = response.url
        basic_item['flat_type'] = meta.get('type')
        basic_item['country'] = meta.get('country')
        basic_item['city'] = meta.get('city')
        basic_item['neighborhood'] = meta.get('neighborhood')

        flats = sel.xpath('//div[@class="items-container"]//article')
        for flat in flats:
            item = copy.deepcopy(basic_item)

            if not flat.xpath('div//@id'):
                item['id'] = flat.xpath('div//@data-adid').extract()[0]

            else:
                logging.debug('Find banner in overview. Ignoring...')
                continue

            info_container = flat.css('.item-info-container')

            item['url'] = '{base_url}{item_url}'.format(
                base_url=self.base_url,
                item_url=info_container.xpath('a//@href').extract()[0]
            )
            item['title'] = info_container.xpath('a//text()').extract()[0]

            yield Request(
                url=item['url'],
                meta={
                    'item': item
                },
                callback=IdealistaSpider.detail
            )

        # PAGINATION
        next_button = sel.css('.next').xpath('a/@href').extract()
        if next_button:
            yield Request(
                url='{base_url}{next_page}'.format(
                    base_url=self.base_url,
                    next_page=next_button[0]
                ),
                meta=meta,
                callback=self.overview
            )

    @staticmethod
    def detail(response):
        sel = Selector(response)

        item = copy.deepcopy(response.meta.get('item'))

        item['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        flat_info = sel.css('.info-data')

        price_info = flat_info.xpath('span')[0]

        item['price_text'] = price_info.xpath('span//text()').extract()[0]
        item['currency'] = price_info.xpath('text()').extract()[0]

        item['square_meters'] = int(flat_info.xpath('span')[1].xpath('span//text()').extract()[0])

        item['rooms'] = flat_info.xpath('span')[2].xpath('span//text()').extract()[0] \
            if flat_info.xpath('span')[2].xpath('span//text()').extract() \
            else 0

        item['floor'] = flat_info.xpath('span')[3].xpath('span//text()').extract()[0] \
            if flat_info.xpath('span')[3].xpath('span//text()').extract() \
            else -1

        main_content = sel.css('#main-content')

        multimedia = main_content.css('#multimedia-container')
        item['image_urls'] = []
        item['image_urls'] += multimedia.css('#main-multimedia').xpath('div/img/@data-service').extract()
        item['image_urls'] += multimedia.css('#grid-multimedia').xpath('div/img/@data-service').extract()

        details = main_content.css('#details')
        item['description'] = details.xpath('div')[0].xpath('div/div/text()').extract()[0]
        item['basic_info'] = details.xpath('div')[2].xpath('ul').extract()[0]
        item['building_info'] = details.xpath('div')[3].xpath('ul').extract()[0] \
            if len(details.xpath('div')) > 3 \
            else None
        item['equipment_info'] = details.xpath('div')[4].xpath('ul').extract()[0] \
            if len(details.xpath('div')) > 4 \
            else None

        yield item

    def parse(self, response):
        pass
