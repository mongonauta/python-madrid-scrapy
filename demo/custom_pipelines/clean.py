class CleanItems(object):
    currency_us = 'USD'
    currency_es = 'EUR'

    def process_item(self, item, spider):
        item['rooms'] = int(item['rooms'])
        item['price_value'] = float(item['price_text'].replace('.', ''))

        if item['country'].lower() == 'spain':
            item['country_code'] = 'ES'

        item['currency_value'] = self.currency_us \
            if '$' in item['currency_text'] \
            else self.currency_es

        return item
