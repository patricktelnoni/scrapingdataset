# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class DatasetItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    title   = scrapy.Field()
    # content = MapCompose(str.strip())
