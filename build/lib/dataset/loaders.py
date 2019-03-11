from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class ScrapingTestingLoader(ItemLoader):
    content = MapCompose(str.strip())
    title   = TakeFirst()