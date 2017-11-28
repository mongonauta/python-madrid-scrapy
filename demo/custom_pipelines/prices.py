class AddUSDToItems(object):
    exchange_rate = 1.19

    def process_item(self, item, spider):
        item['price_value_usd'] = item['price_value'] * self.exchange_rate

        return item
