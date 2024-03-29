# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviejwtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'bookjwt'

    score = scrapy.Field()
    name = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    authors = scrapy.Field()
    published_at = scrapy.Field()
    isbm = scrapy.Field()
    cover = scrapy.Field()
    comments = scrapy.Field()
    image_paths = scrapy.Field()
