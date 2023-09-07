# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


class Prothomalo2Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(input_processor = MapCompose(remove_tags))
    url = scrapy.Field()
    story = scrapy.Field()

    pass
