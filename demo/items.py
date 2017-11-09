from scrapy.item import Item, Field


class FlatItem(Item):
    # DEFAULT INFO
    website = Field(type="str")
    referer_url = Field(type="str")
    flat_type = Field(type="str")
    country = Field(type="str")
    city = Field(type="str")
    neighborhood = Field(type="str")

    # BASIC INFO
    id = Field(type="str")
    url = Field(type="str")
    title = Field(type="str")

    # DETAILS INFO
    timestamp = Field(type="str")

    price_text = Field(type="str")
    currency = Field(type="str")

    rooms = Field(type="int")
    square_meters = Field(type="int")
    floor = Field(type="int")

    image_urls = Field(type="list")
    description = Field(type="str")
    basic_info = Field(type="str")
    building_info = Field(type="str")
    equipment_info = Field(type="str")

    # CALCULATED INFO
    country_code = Field(type="str")
    price_value = Field(type="int")
