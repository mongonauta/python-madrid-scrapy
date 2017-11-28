class AddItemStats(object):
    def process_item(self, item, spider):
        if not spider.cache_info:
            spider.cache_info = {
                'square_meters': [],
                'prices': [],
                'rooms': [],
            }

        spider.cache_info['square_meters'].append(item['square_meters'])
        spider.cache_info['prices'].append(item['price_value'])

        if item['rooms'] > 0:
            spider.cache_info['rooms'].append(item['rooms'])

        return item
